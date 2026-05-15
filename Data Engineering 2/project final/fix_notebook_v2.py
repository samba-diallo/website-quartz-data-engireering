import json

with open("DE2_Project_Notebook_EN.ipynb", "r") as f:
    nb = json.load(f)

# Fix Cell 7 (process_silver)
c7_source = """# 1.2 Couche Silver (Nettoyage et Application du Schéma)
def process_silver():
    print("Démarrage du traitement de la couche Silver...")
    import time
    t0 = time.time()
    bronze_df = spark.read.parquet(CFG["paths"]["bronze"])
    
    # Filtrer les identifiants vides et sélectionner les colonnes importantes
    # Extraction des structures JSON imbriquées
    silver_df = bronze_df.filter(F.col("id").isNotNull()) \\
        .select(
            F.col("id").alias("event_id"),
            F.col("type").alias("event_type"),
            F.col("actor.login").alias("actor_login"),
            F.col("repo.name").alias("repo_name"),
            F.col("created_at").cast("timestamp").alias("created_at"),
            F.to_date(F.col("created_at")).alias("date"),
            F.col("payload.commits").alias("commits"),
            F.coalesce(F.col("payload.pull_request.body"), F.col("payload.pull_request.title")).alias("pr_text")
        )
    
    # Partitionner par date et sauvegarder
    silver_df.write.mode("overwrite") \\
        .partitionBy(*CFG["layout"]["partition_by"]) \\
        .parquet(CFG["paths"]["silver"])
    
    t1 = time.time()
    record_metric("Batch ETL", "silver_latency_sec", t1 - t0, f"Nettoyage de {silver_df.count()} évènements")
    print(f"Couche Silver terminée en {t1 - t0:.2f} secondes.")
    return silver_df"""

nb["cells"][7]["source"] = [line + "\n" for line in c7_source.split("\n")]
if nb["cells"][7]["source"][-1].endswith("\n\n"):
    nb["cells"][7]["source"][-1] = nb["cells"][7]["source"][-1][:-1]

# Fix Cell 20 (Phase 3 text corpus)
c20_source = """# 3.1 Extraction du corpus texte (messages de commit)
t0_text = time.time()
silver_df = spark.read.parquet(CFG["paths"]["silver"])

# Extraire les messages de commit depuis le tableau 'commits'
corpus = silver_df.filter(F.col("event_type") == "PushEvent") \\
    .withColumn("commit", F.explode("commits")) \\
    .select(
        F.col("commit.sha").alias("doc_id"),
        F.col("commit.message").alias("text")
    ).filter(F.col("text").isNotNull() & (F.length("text") > 0))

print(f"Documents dans le corpus : {corpus.count()}")
corpus.show(5)"""
nb["cells"][20]["source"] = [line + "\n" for line in c20_source.split("\n")]
if nb["cells"][20]["source"][-1].endswith("\n\n"):
    nb["cells"][20]["source"][-1] = nb["cells"][20]["source"][-1][:-1]

# Fix Cell 30 (Phase 5 LLM corpus)
c30_source = """# 5.1 Extraction et curation du dataset LLM
t0_llm = time.time()

# Combiner plusieurs sources de texte pour le dataset LLM
pr_text = silver_df.filter(F.col("event_type") == "PullRequestEvent") \\
    .select(
        F.col("event_id").alias("doc_id"), 
        F.col("pr_text").alias("text")
    )

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
print(f"Taux de passage    : {pass_rate:.1f}% (SLO >= 80%)")"""
nb["cells"][30]["source"] = [line + "\n" for line in c30_source.split("\n")]
if nb["cells"][30]["source"][-1].endswith("\n\n"):
    nb["cells"][30]["source"][-1] = nb["cells"][30]["source"][-1][:-1]

with open("DE2_Project_Notebook_EN.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook fixes applied!")
