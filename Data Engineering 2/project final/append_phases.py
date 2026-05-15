import json

with open("DE2_Project_Notebook_EN.ipynb", "r") as f:
    nb = json.load(f)

def add_md(text):
    nb["cells"].append({"cell_type": "markdown", "metadata": {}, "source": [text]})

def add_code(text):
    lines = [line + "\n" for line in text.split("\n")]
    if lines and lines[-1].endswith("\n"):
        lines[-1] = lines[-1][:-1]
    nb["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": lines})

# Remove any cells after index 18 (if any exist, but we know there are exactly 19 cells: indices 0-18)
nb["cells"] = nb["cells"][:19]

add_md("""## Phase 3 : Pipeline Texte — Index Inversé

Extraction des messages de commit (`PushEvent`), tokenisation, normalisation, et construction d'un **index inversé**.
Cela permet de mesurer la latence de requête et l'empreinte disque.""")

add_code("""# 3.1 Extraction du corpus texte (messages de commit)
t0_text = time.time()
silver_df = spark.read.parquet(CFG["paths"]["silver"])

# Extraire les messages de commit depuis le payload JSON
corpus = silver_df.filter(F.col("event_type") == "PushEvent") \\
    .withColumn("commit", F.explode(F.from_json("payload", "ARRAY<STRUCT<message:STRING, sha:STRING>>", {"allowUnquotedFieldNames":"true"}))) \\
    .select(
        F.col("commit.sha").alias("doc_id"),
        F.col("commit.message").alias("text")
    ).filter(F.col("text").isNotNull() & (F.length("text") > 0))

print(f"Documents dans le corpus : {corpus.count()}")
corpus.show(5)""")

add_code("""# 3.2 Tokenisation, normalisation, suppression des stop-words
stop_words = {"the","a","an","is","it","to","in","of","and","for","on","with","as","by","at","this","that","from"}

tokens = corpus.withColumn("text_clean", F.regexp_replace(F.lower(F.col("text")), r"[^a-z0-9\\s]", " ")) \\
    .withColumn("tokens", F.split("text_clean", r"\\s+")) \\
    .select("doc_id", F.explode("tokens").alias("token")) \\
    .filter((F.length("token") > 1) & (~F.col("token").isin(stop_words)))

print(f"Tokens apres nettoyage : {tokens.count()}")""")

add_code("""# 3.3 Construction de l'index inverse
inverted_index = tokens.groupBy("token") \\
    .agg(
        F.collect_list("doc_id").alias("doc_ids"),
        F.count("doc_id").alias("freq")
    ).orderBy(F.desc("freq"))

inverted_index.write.mode("overwrite").parquet(CFG["paths"]["text"])
print(f"Termes uniques dans l'index : {inverted_index.count()}")""")

add_code("""# 3.4 Mesure de latence de requete (SLO <= 2s)
idx = spark.read.parquet(CFG["paths"]["text"])
idx.cache()
idx.count() # Force l'evaluation

query_terms = CFG["text"]["query_terms"]
for term in query_terms:
    t0_q = time.time()
    res = idx.filter(F.col("token") == term).collect()
    t_ms = (time.time() - t0_q) * 1000
    docs = len(res[0]['doc_ids']) if res else 0
    record_metric("Text", f"query_latency_{term}_ms", t_ms, f"Found {docs} docs")
    print(f"Requete '{term}': {t_ms:.1f} ms (Trouve dans {docs} documents)")
""")

add_code("""# 3.5 Comparaison empreinte Parquet vs CSV
import pathlib
import os

# Sauvegarder aussi en CSV pour comparer
csv_path = CFG["paths"]["text"] + "_csv"
inverted_index.write.mode("overwrite").option("header", "true").csv(csv_path)

def get_size(path):
    return sum(f.stat().st_size for f in pathlib.Path(path).glob('**/*') if f.is_file())

size_parquet = get_size(CFG["paths"]["text"])
size_csv = get_size(csv_path)
ratio = (size_parquet / size_csv) * 100 if size_csv > 0 else 0

record_metric("Text", "storage_ratio_pct", ratio, "Parquet vs CSV")
print(f"Taille CSV     : {size_csv / 1024 / 1024:.2f} MB")
print(f"Taille Parquet : {size_parquet / 1024 / 1024:.2f} MB")
print(f"Ratio Parquet/CSV : {ratio:.1f}% (SLO <= 60%)")
""")

add_md("""## Phase 4 : Charge Itérative — Graphe & PageRank

Construction d'un graphe des interactions **(Développeur → Dépôt)** et calcul du **PageRank** pour identifier les dépôts les plus influents.
L'algorithme tourne via des jointures itératives, ce qui permet de mesurer le coût du *shuffle* et la convergence à chaque étape.""")

add_code("""# 4.1 Construction du graphe (Acteur -> Dépôt)
# On s'intéresse aux événements de contribution (Push, PR, Issues)
contribution_events = ["PushEvent", "PullRequestEvent", "IssuesEvent"]

edges = silver_df.filter(F.col("event_type").isin(contribution_events)) \\
    .select(
        F.col("actor_login").alias("src"),
        F.col("repo_name").alias("dst")
    ).distinct().cache()

# Calculer le degré sortant (out-degree) de chaque acteur
out_degree = edges.groupBy("src").count().withColumnRenamed("count", "out_deg").cache()

print(f"Nombre d'arêtes (interactions uniques) : {edges.count()}")
""")

add_code("""# 4.2 PageRank Itératif
t0_pr = time.time()
MAX_ITER = CFG.get("pagerank", {}).get("max_iter", 10)
DAMPING = CFG.get("pagerank", {}).get("damping", 0.85)

# Nœuds uniques (acteurs et dépôts combinés)
vertices = edges.select("src").union(edges.select(F.col("dst").alias("src"))).distinct().cache()
N = vertices.count()

# Initialisation : chaque nœud commence avec un rang de 1/N
ranks = vertices.withColumn("rank", F.lit(1.0 / N))

for i in range(MAX_ITER):
    # Calculer les contributions : rank_source / out_degree_source
    contribs = edges.join(ranks, "src") \\
        .join(out_degree, "src") \\
        .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
    
    # Mettre à jour les rangs : (1 - d)/N + d * sum(contributions)
    new_ranks = contribs.groupBy("src").agg(
        (F.lit(1 - DAMPING) / N + DAMPING * F.sum("contrib")).alias("rank")
    ).cache()
    
    # Calculer la convergence (différence absolue totale)
    delta = ranks.join(new_ranks, "src", "full_outer") \\
        .select(F.abs(F.coalesce(ranks["rank"], F.lit(0)) - F.coalesce(new_ranks["rank"], F.lit(0))).alias("diff")) \\
        .agg(F.sum("diff")).collect()[0][0]
    
    record_metric("Iterative", f"pagerank_delta", delta, f"Iteration {i+1}")
    print(f"Itération {i+1} - Delta : {delta:.6f}")
    
    ranks = new_ranks

# Sauvegarder les résultats
pr_output = os.path.join(CFG["paths"]["gold"], "pagerank")
ranks.orderBy(F.desc("rank")).write.mode("overwrite").parquet(pr_output)

t1_pr = time.time()
record_metric("Iterative", "pagerank_latency_sec", t1_pr - t0_pr, f"{MAX_ITER} itérations")
print(f"PageRank terminé en {t1_pr - t0_pr:.2f} secondes. Top 10 influents :")
ranks.orderBy(F.desc("rank")).show(10, truncate=False)
""")

add_code("""# 4.3 Expérience de partitionnement
# Test de la configuration "optimisée" en repartitionnant par hachage
t0_opt = time.time()
edges_opt = edges.repartition(CFG["spark"]["partitions"], "src").cache()
out_degree_opt = edges_opt.groupBy("src").count().withColumnRenamed("count", "out_deg").cache()

ranks_opt = vertices.withColumn("rank", F.lit(1.0 / N))

for i in range(2): # Juste 2 itérations pour le test de temps
    contribs = edges_opt.join(ranks_opt, "src") \\
        .join(out_degree_opt, "src") \\
        .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
    
    ranks_opt = contribs.groupBy("src").agg(
        (F.lit(1 - DAMPING) / N + DAMPING * F.sum("contrib")).alias("rank")
    ).cache()
    ranks_opt.count() # Force execution

t1_opt = time.time()
record_metric("Iterative", "pagerank_opt_latency_sec", t1_opt - t0_opt, "2 itérations optimisées")
print(f"Temps avec partitionnement optimisé (2 iters) : {t1_opt - t0_opt:.2f}s")
""")

add_md("""## Phase 5 : Préparation LLM (Data Readiness)

Préparation d'un dataset "curaté" pour un LLM (RAG ou Fine-Tuning).
On applique des filtres de qualité (longueur minimale, déduplication par hash).""")

add_code("""# 5.1 Extraction et curation du dataset LLM
t0_llm = time.time()

# Combiner plusieurs sources de texte pour le dataset LLM
pr_text = silver_df.filter(F.col("event_type") == "PullRequestEvent") \\
    .select(F.col("event_id").alias("doc_id"), F.col("payload").alias("text"))

llm_corpus = corpus.unionByName(pr_text) # Push messages + PR payloads

min_len = CFG.get("llm", {}).get("min_text_length", 50)

# Filtres qualité : longueur minimale, déduplication exacte (par hash)
df_llm = llm_corpus.filter(F.col("text").isNotNull()) \\
    .filter(F.length("text") >= min_len) \\
    .withColumn("content_hash", F.xxhash64("text")) \\
    .dropDuplicates(["content_hash"]) \\
    .withColumn("source", F.lit("github_archive")) \\
    .withColumn("version", F.lit("v1.0")) \\
    .withColumn("curated_at", F.current_timestamp())

# Sauvegarde
df_llm.write.mode("overwrite").parquet(CFG["paths"]["llm_ready"])

# Mesure de qualité
total_initial = llm_corpus.count()
total_curated = df_llm.count()
pass_rate = (total_curated / total_initial * 100) if total_initial > 0 else 0

record_metric("LLM", "quality_pass_rate_pct", pass_rate, f"Pass rate, min_len={min_len}")
print(f"Documents initiaux : {total_initial}")
print(f"Documents validés  : {total_curated}")
print(f"Taux de passage    : {pass_rate:.1f}% (SLO >= 80%)")
""")

add_md("""## Phase 6 : Optimisation Physique

Examen des plans `EXPLAIN FORMATTED` et sauvegarde des preuves. Compaction et réduction du *shuffle*.""")

add_code("""# 6.1 Plans EXPLAIN et optimisation
import os
os.makedirs(CFG["paths"]["proof"], exist_ok=True)

# Capturer le plan d'une requête analytique Gold
q_gold = spark.read.parquet(CFG["paths"]["gold"] + "/repo_activity") \\
    .groupBy("repo_name").agg(F.sum("event_count").alias("total")) \\
    .orderBy(F.desc("total"))

plan_str = q_gold._jdf.queryExecution().explainString(org.apache.spark.sql.execution.ExplainMode.fromString("formatted"))

with open(os.path.join(CFG["paths"]["proof"], "plan_gold_query.txt"), "w") as f:
    f.write(plan_str)

# Capturer le plan d'une itération PageRank
contribs = edges.join(ranks, "src").join(out_degree, "src") \\
    .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
plan_pr = contribs._jdf.queryExecution().explainString(org.apache.spark.sql.execution.ExplainMode.fromString("formatted"))

with open(os.path.join(CFG["paths"]["proof"], "plan_iterative_pagerank.txt"), "w") as f:
    f.write(plan_pr)

print("Plans d'exécution sauvegardés dans le dossier proof/.")
""")

add_md("""## Phase 7 : Preuves et Arrêt

Affichage des métriques collectées et arrêt propre du cluster Spark.""")

add_code("""# 7.1 Vérification des SLOs et résumé
print("=" * 60)
print("RESUME DU PIPELINE DE2 — GitHub Archive (Track B)")
print("=" * 60)

import pandas as pd
df_metrics = pd.read_csv(CFG["paths"]["metrics_log"])
print(df_metrics.tail(15)[["stage", "metric_name", "metric_value"]].to_string())

spark.stop()
print("\\nSession Spark arrêtée avec succès. N'oubliez pas de capturer vos captures d'écran Spark UI !")
""")

with open("DE2_Project_Notebook_EN.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Cells appended successfully!")
