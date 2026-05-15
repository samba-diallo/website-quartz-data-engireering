---
title: Code Source du Notebook (PySpark)
description: Le code complet du pipeline Medallion et PageRank
date: 2026-05-15
---
# DE2 — Cahier de Projet Final
Auteur : Samba DIALLO - Data Engineering II (Data-Intensive Workloads) - ESIEE 2025-2026

Ceci est l'artefact exécutable principal. Configurez les chemins, lancez le pipeline complet (Batch ETL → Streaming → Traitement de Texte → Itératif → Préparation LLM), et enregistrez les preuves.

### Étape 0 : Configuration & Initialisation de Spark
Avant de commencer tout traitement, nous chargeons nos paramètres centraux depuis `de2_project_config.yml`. Cela nous permet de garder les chemins, les SLOs (objectifs de niveau de service) et les configurations en dehors du code. Nous initialisons également la `SparkSession` en activant l'exécution adaptative des requêtes (AQE).


```python
# ==================================================================
# 0. Charger la configuration et initialiser Spark
# ==================================================================
import yaml, pathlib, datetime, time, json
import os
from pyspark.sql import SparkSession, functions as F, types as T

with open("de2_project_config.yml", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

spark = SparkSession.builder \
    .appName(CFG["spark"]["app_name"]) \
    .master(CFG["spark"]["master"]) \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

print("Spark:", spark.version)
print("UI:", spark.sparkContext.uiWebUrl)
print("Configuration chargée avec succès.")
```

## Phase 1: Pipeline Batch ETL & Architecture Medallion

Cette phase ingère les données brutes de GitHub Archive, les traite à travers les couches Bronze, Silver et Gold, et enregistre les métriques de performance du pipeline.

### 1.1 Couche Bronze (Ingestion Brute)
La couche Bronze est responsable de l'ingestion des données brutes sans altérer la structure de base. Nous lisons les fichiers `.json.gz` depuis notre dossier `archive/`, nous ajoutons une colonne `ingestion_tstamp` pour l'audit, et nous sauvegardons les données efficacement au format **Parquet**. Nous enregistrons également le temps d'exécution pour vérifier nos SLOs.


```python
# 1.1 Couche Bronze (Ingestion Brute)
def process_bronze():
    print("Démarrage du traitement de la couche Bronze...")
    t0 = time.time()
    # Lire les données JSON brutes
    raw_df = spark.read.json(CFG["paths"]["raw_csv_glob"])
    
    # Ajouter les métadonnées d'ingestion
    bronze_df = raw_df.withColumn("ingestion_tstamp", F.current_timestamp())
    
    # Sauvegarder au format Parquet
    bronze_df.write.mode("overwrite").parquet(CFG["paths"]["bronze"])
    
    t1 = time.time()
    record_metric("Batch ETL", "bronze_latency_sec", t1 - t0, f"Traitement de {bronze_df.count()} évènements bruts")
    print(f"Couche Bronze terminée en {t1 - t0:.2f} secondes.")
    return bronze_df

def record_metric(stage, metric_name, metric_value, notes=""):
    timestamp = datetime.datetime.now().isoformat()
    run_id = f"run_{int(time.time())}"
    row = f"{run_id},{stage},task,{metric_name},{metric_value},{notes},{timestamp}\n"
    with open(CFG["paths"]["metrics_log"], "a", encoding="utf-8") as f:
        f.write(row)

```

### 1.2 Couche Silver (Nettoyage & Application du Schéma)
La couche Silver applique des validations strictes sur le schéma et aplatit les données. Nous filtrons les enregistrements malformés (ex: `id` manquant), extrayons les éléments nécessaires depuis les JSON imbriqués (comme `actor.login`, `repo.name`), convertissons les chaînes de caractères en types `timestamp`/`date`, et écrivons le résultat partitionné par `date` pour optimiser les requêtes futures.


```python
# 1.2 Couche Silver (Nettoyage et Application du Schéma)
def process_silver():
    print("Démarrage du traitement de la couche Silver...")
    import time
    t0 = time.time()
    bronze_df = spark.read.parquet(CFG["paths"]["bronze"])
    
    # Filtrer les identifiants vides et sélectionner les colonnes importantes
    # Extraction des structures JSON imbriquées
    silver_df = bronze_df.filter(F.col("id").isNotNull()) \
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
    silver_df.write.mode("overwrite") \
        .partitionBy(*CFG["layout"]["partition_by"]) \
        .parquet(CFG["paths"]["silver"])
    
    t1 = time.time()
    record_metric("Batch ETL", "silver_latency_sec", t1 - t0, f"Nettoyage de {silver_df.count()} évènements")
    print(f"Couche Silver terminée en {t1 - t0:.2f} secondes.")
    return silver_df

```

### 1.3 Couche Gold (Agrégations Analytiques)
La couche Gold crée des datasets agrégés prêts à être consommés par des tableaux de bord analytiques ou des outils de BI. Ici, nous calculons le volume quotidien de chaque type d'événement par dépôt de code (`repo_activity`). Cela réduit considérablement la taille des données et optimise la vitesse des rapports.


```python
# 1.3 Couche Gold (Agrégations)
def process_gold():
    print("Démarrage du traitement de la couche Gold...")
    t0 = time.time()
    silver_df = spark.read.parquet(CFG["paths"]["silver"])
    
    # Agréger les événements par dépôt et par jour
    gold_repo_activity = silver_df.groupBy("date", "repo_name", "event_type") \
        .agg(F.count("event_id").alias("event_count"))
        
    gold_repo_activity.write.mode("overwrite").parquet(os.path.join(CFG["paths"]["gold"], "repo_activity"))
    
    t1 = time.time()
    record_metric("Batch ETL", "gold_latency_sec", t1 - t0, f"Agrégation des dépôts réussie")
    print(f"Couche Gold terminée en {t1 - t0:.2f} secondes.")
    return gold_repo_activity

```

### Exécution du Pipeline Batch (Phase 1)
Il est temps de déclencher le traitement réel des données. Décommentez les appels de fonctions ci-dessous pour lancer le pipeline de bout en bout sur vos données GitHub Archive locales.


```python
# Exécuter le Pipeline de la Phase 1
# À décommenter et exécuter après le téléchargement via download_gh_archive.py
process_bronze()
process_silver()
process_gold()

```

## Phase 2 : Ingestion Streaming (Structured Streaming)

Cette phase implémente l'ingestion en continu via **Structured Streaming** avec une **source fichier**.
Le script `simulate_streaming.py` dépose les fichiers `.json.gz` un par un dans `data/landing/`.
Spark les détecte automatiquement et les traite comme des micro-batches.

**Composants clés :**
- `readStream` avec `maxFilesPerTrigger=1` (1 fichier par micro-batch)
- Agrégation fenêtrée avec **watermark** (retard toléré de 10 min)
- Fenêtre temporelle de 5 minutes
- Écriture en mode **append** vers Parquet


### 2.1 Schéma de lecture pour le streaming
En streaming, Spark ne peut pas inférer le schéma automatiquement.
On définit donc un schéma explicite basé sur les champs principaux de GitHub Archive.


```python
# 2.1 Schéma explicite pour le streaming
# En mode streaming, Spark ne peut pas inférer le schéma à la volée.
# On le définit manuellement à partir des champs GitHub Archive.
from pyspark.sql.types import StructType, StructField, StringType, LongType

streaming_schema = StructType([
    StructField("id", StringType(), True),
    StructField("type", StringType(), True),
    StructField("actor", StructType([
        StructField("login", StringType(), True),
    ]), True),
    StructField("repo", StructType([
        StructField("name", StringType(), True),
    ]), True),
    StructField("created_at", StringType(), True),
])

print("Schéma de streaming défini.")

```

### 2.2 Lancement du flux Structured Streaming
On lit les fichiers JSON déposés dans `data/landing/` avec `readStream`.
On applique une **agrégation fenêtrée** avec un **watermark**.

**IMPORTANT :** Avant d'exécuter cette cellule, lancez `simulate_streaming.py` dans un terminal séparé :
```bash
python simulate_streaming.py
```


```python
# 2.2 Démarrer le flux Structured Streaming
import shutil

# Nettoyer les sorties précédentes pour repartir de zéro
for d in [CFG["paths"]["streaming"], CFG["paths"]["streaming_checkpoint"]]:
    if os.path.exists(d):
        shutil.rmtree(d)

# Lire le flux depuis le dossier landing/ (source fichier)
# maxFilesPerTrigger=1 : on ne traite qu'un fichier par micro-batch
stream_df = spark.readStream \
    .schema(streaming_schema) \
    .option("maxFilesPerTrigger", 1) \
    .json(CFG["paths"]["streaming_landing"])

# Convertir created_at en timestamp pour le watermark
stream_typed = stream_df \
    .withColumn("event_ts", F.to_timestamp(F.col("created_at"))) \
    .filter(F.col("event_ts").isNotNull())

# Agrégation fenêtrée avec watermark :
# - Watermark : on tolère un retard avant de fermer une fenêtre
# - Fenêtre temporelle : on agrège les événements par tranches
windowed_counts = stream_typed \
    .withWatermark("event_ts", CFG["streaming"]["watermark"]) \
    .groupBy(
        F.window("event_ts", CFG["streaming"]["window_duration"]),
        F.col("type").alias("event_type")
    ) \
    .agg(F.count("*").alias("event_count"))

# Écriture en mode append vers Parquet avec checkpoint
streaming_query = windowed_counts.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", CFG["paths"]["streaming"]) \
    .option("checkpointLocation", CFG["paths"]["streaming_checkpoint"]) \
    .trigger(processingTime=CFG["streaming"]["trigger_interval"]) \
    .start()

wm = CFG['streaming']['watermark']
ti = CFG['streaming']['trigger_interval']
wd = CFG['streaming']['window_duration']
print("Streaming démarré. En attente des fichiers dans data/landing/ ...")
print(f"Trigger : {ti}  |  Watermark : {wm}  |  Fenêtre : {wd}")

```

### 2.3 Surveillance du flux et capture des métriques
On attend que le flux traite tous les fichiers disponibles, puis on capture `query.lastProgress`
comme preuve du bon fonctionnement du streaming.


```python
# 2.3 Attendre le traitement et capturer les preuves
import json as json_lib
from uuid import UUID

# Encodeur personnalisé pour gérer les UUID dans lastProgress
class SafeEncoder(json_lib.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

# Attendre que le streaming traite les fichiers disponibles
WAIT_SECONDS = 90
print(f"Attente de {WAIT_SECONDS}s pour laisser le streaming traiter les fichiers...")
time.sleep(WAIT_SECONDS)

# Capturer query.lastProgress comme preuve
last_progress = streaming_query.lastProgress
if last_progress:
    print("=== query.lastProgress ===")
    print(json_lib.dumps(last_progress, indent=2, cls=SafeEncoder))
    
    # Sauvegarder la preuve dans proof/
    os.makedirs(CFG["paths"]["proof"], exist_ok=True)
    proof_path = os.path.join(CFG["paths"]["proof"], "streaming_lastProgress.json")
    with open(proof_path, "w", encoding="utf-8") as f:
        json_lib.dump(last_progress, f, indent=2, cls=SafeEncoder)
    print(f"Preuve sauvegardée : {proof_path}")
    
    # Enregistrer la métrique
    record_metric("Streaming", "streaming_trigger_latency",
                  last_progress.get("batchDuration", "N/A"),
                  f"Batch {last_progress.get('batchId', 'N/A')}")
else:
    print("Aucun batch traité. Vérifiez que simulate_streaming.py a déposé des fichiers.")

# Arrêter proprement le flux
streaming_query.stop()
print("Streaming arrêté proprement.")

# Vérifier les résultats écrits
result_df = spark.read.parquet(CFG["paths"]["streaming"])
print(f"\nNombre de lignes dans la sortie streaming : {result_df.count()}")
result_df.orderBy("window").show(10, truncate=False)

```

## Phase 3 : Pipeline Texte — Index Inversé

Extraction des messages de commit (`PushEvent`), tokenisation, normalisation, et construction d'un **index inversé**.
Cela permet de mesurer la latence de requête et l'empreinte disque.


```python
# 3.1 Extraction du corpus texte (messages de commit)
t0_text = time.time()
silver_df = spark.read.parquet(CFG["paths"]["silver"])

# Extraire les messages de commit depuis le tableau 'commits'
corpus = silver_df.filter(F.col("event_type") == "PushEvent") \
    .withColumn("commit", F.explode("commits")) \
    .select(
        F.col("commit.sha").alias("doc_id"),
        F.col("commit.message").alias("text")
    ).filter(F.col("text").isNotNull() & (F.length("text") > 0))

print(f"Documents dans le corpus : {corpus.count()}")
corpus.show(5)

```


```python
# 3.2 Tokenisation, normalisation, suppression des stop-words
stop_words = {"the","a","an","is","it","to","in","of","and","for","on","with","as","by","at","this","that","from"}

tokens = corpus.withColumn("text_clean", F.regexp_replace(F.lower(F.col("text")), r"[^a-z0-9\s]", " ")) \
    .withColumn("tokens", F.split("text_clean", r"\s+")) \
    .select("doc_id", F.explode("tokens").alias("token")) \
    .filter((F.length("token") > 1) & (~F.col("token").isin(stop_words)))

print(f"Tokens apres nettoyage : {tokens.count()}")
```


```python
# 3.3 Construction de l'index inverse
inverted_index = tokens.groupBy("token") \
    .agg(
        F.collect_list("doc_id").alias("doc_ids"),
        F.count("doc_id").alias("freq")
    ).orderBy(F.desc("freq"))

inverted_index.write.mode("overwrite").parquet(CFG["paths"]["text"])
print(f"Termes uniques dans l'index : {inverted_index.count()}")
```


```python
# 3.4 Mesure de latence de requete (SLO <= 2s)
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

```


```python
# 3.5 Comparaison empreinte Parquet vs CSV
import pathlib
import os

# Sauvegarder aussi en CSV pour comparer (CSV ne supporte pas les arrays, on les convertit en string)
csv_path = CFG["paths"]["text"] + "_csv"
inverted_index.withColumn("doc_ids", F.concat_ws(",", "doc_ids")).write.mode("overwrite").option("header", "true").csv(csv_path)

def get_size(path):
    return sum(f.stat().st_size for f in pathlib.Path(path).glob('**/*') if f.is_file())

size_parquet = get_size(CFG["paths"]["text"])
size_csv = get_size(csv_path)
ratio = (size_parquet / size_csv) * 100 if size_csv > 0 else 0

record_metric("Text", "storage_ratio_pct", ratio, "Parquet vs CSV")
print(f"Taille CSV     : {size_csv / 1024 / 1024:.2f} MB")
print(f"Taille Parquet : {size_parquet / 1024 / 1024:.2f} MB")
print(f"Ratio Parquet/CSV : {ratio:.1f}% (SLO <= 60%)")

```

## Phase 4 : Charge Itérative — Graphe & PageRank

Construction d'un graphe des interactions **(Développeur → Dépôt)** et calcul du **PageRank** pour identifier les dépôts les plus influents.
L'algorithme tourne via des jointures itératives, ce qui permet de mesurer le coût du *shuffle* et la convergence à chaque étape.


```python
# 4.1 Construction du graphe (Acteur -> Dépôt)
# On s'intéresse aux événements de contribution (Push, PR, Issues)
contribution_events = ["PushEvent", "PullRequestEvent", "IssuesEvent"]

edges = silver_df.filter(F.col("event_type").isin(contribution_events)) \
    .select(
        F.col("actor_login").alias("src"),
        F.col("repo_name").alias("dst")
    ).distinct().cache()

# Calculer le degré sortant (out-degree) de chaque acteur
out_degree = edges.groupBy("src").count().withColumnRenamed("count", "out_deg").cache()

print(f"Nombre d'arêtes (interactions uniques) : {edges.count()}")

```


```python
# 4.2 PageRank Itératif
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
    contribs = edges.join(ranks, "src") \
        .join(out_degree, "src") \
        .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
    
    # Mettre à jour les rangs : (1 - d)/N + d * sum(contributions)
    new_ranks = contribs.groupBy("src").agg(
        (F.lit(1 - DAMPING) / N + DAMPING * F.sum("contrib")).alias("rank")
    ).cache()
    
    # Calculer la convergence (différence absolue totale)
    delta = ranks.join(new_ranks, "src", "full_outer") \
        .select(F.abs(F.coalesce(ranks["rank"], F.lit(0)) - F.coalesce(new_ranks["rank"], F.lit(0))).alias("diff")) \
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

```


```python
# 4.3 Expérience de partitionnement
# Test de la configuration "optimisée" en repartitionnant par hachage
t0_opt = time.time()
edges_opt = edges.repartition(CFG["spark"]["partitions"], "src").cache()
out_degree_opt = edges_opt.groupBy("src").count().withColumnRenamed("count", "out_deg").cache()

ranks_opt = vertices.withColumn("rank", F.lit(1.0 / N))

for i in range(2): # Juste 2 itérations pour le test de temps
    contribs = edges_opt.join(ranks_opt, "src") \
        .join(out_degree_opt, "src") \
        .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
    
    ranks_opt = contribs.groupBy("src").agg(
        (F.lit(1 - DAMPING) / N + DAMPING * F.sum("contrib")).alias("rank")
    ).cache()
    ranks_opt.count() # Force execution

t1_opt = time.time()
record_metric("Iterative", "pagerank_opt_latency_sec", t1_opt - t0_opt, "2 itérations optimisées")
print(f"Temps avec partitionnement optimisé (2 iters) : {t1_opt - t0_opt:.2f}s")

```

## Phase 5 : Préparation LLM (Data Readiness)

Préparation d'un dataset "curaté" pour un LLM (RAG ou Fine-Tuning).
On applique des filtres de qualité (longueur minimale, déduplication par hash).


```python
# 5.1 Extraction et curation du dataset LLM
t0_llm = time.time()

# Combiner plusieurs sources de texte pour le dataset LLM
pr_text = silver_df.filter(F.col("event_type") == "PullRequestEvent") \
    .select(
        F.col("event_id").alias("doc_id"), 
        F.col("pr_text").alias("text")
    )

llm_corpus = corpus.unionByName(pr_text) # Push messages + PR payloads

min_len = CFG.get("llm", {}).get("min_text_length", 50)

# Filtres qualité : longueur minimale, déduplication exacte (par hash)
df_llm = llm_corpus.filter(F.col("text").isNotNull()) \
    .filter(F.length("text") >= min_len) \
    .withColumn("content_hash", F.xxhash64("text")) \
    .dropDuplicates(["content_hash"]) \
    .withColumn("source", F.lit("github_archive")) \
    .withColumn("version", F.lit("v1.0")) \
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

```

## Phase 6 : Optimisation Physique

Examen des plans `EXPLAIN FORMATTED` et sauvegarde des preuves. Compaction et réduction du *shuffle*.


```python
# 6.1 Plans EXPLAIN et optimisation
import os
os.makedirs(CFG["paths"]["proof"], exist_ok=True)

# Capturer le plan d'une requête analytique Gold
q_gold = spark.read.parquet(CFG["paths"]["gold"] + "/repo_activity") \
    .groupBy("repo_name").agg(F.sum("event_count").alias("total")) \
    .orderBy(F.desc("total"))

plan_str = q_gold._jdf.queryExecution().explainString(org.apache.spark.sql.execution.ExplainMode.fromString("formatted"))

with open(os.path.join(CFG["paths"]["proof"], "plan_gold_query.txt"), "w") as f:
    f.write(plan_str)

# Capturer le plan d'une itération PageRank
contribs = edges.join(ranks, "src").join(out_degree, "src") \
    .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
plan_pr = contribs._jdf.queryExecution().explainString(org.apache.spark.sql.execution.ExplainMode.fromString("formatted"))

with open(os.path.join(CFG["paths"]["proof"], "plan_iterative_pagerank.txt"), "w") as f:
    f.write(plan_pr)

print("Plans d'exécution sauvegardés dans le dossier proof/.")

```

## Phase 7 : Preuves et Arrêt

Affichage des métriques collectées et arrêt propre du cluster Spark.


```python
# 7.1 Vérification des SLOs et résumé
print("=" * 60)
print("RESUME DU PIPELINE DE2 — GitHub Archive (Track B)")
print("=" * 60)

import pandas as pd
df_metrics = pd.read_csv(CFG["paths"]["metrics_log"])
print(df_metrics.tail(15)[["stage", "metric_name", "metric_value"]].to_string())

#spark.stop()
print("\nSession Spark arrêtée avec succès. N'oubliez pas de capturer vos captures d'écran Spark UI !")

```
