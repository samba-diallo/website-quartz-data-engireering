



E2 — Final Project (30%): Data-Intensive Pipeline + Evidence
Author : Badr TAJINI - Data Engineering II (Data-Intensive Workloads) - ESIEE 2025-2026

Objective. Build an end-to-end data-intensive pipeline combining batch ETL, streaming ingestion, text processing, iterative computation (graph or clustering), and LLM data readiness on one dataset. Deliver a reproducible pipeline from raw ingestion to curated outputs, with evidence by plans, metrics, and a technical report.

Scope.

Track dataset from Labs 1–3: A (Esports/OpenDota), B (Open-Source/GitHub Archive), C (Micromobility/Citi Bike), or D (Aviation/OpenSky).
Platform: single machine. PySpark (Spark 4.x), Parquet, Structured Streaming, MLlib (clustering only). No external warehouses required.
Minimum ≥ 10M rows or ≥ 3 GB raw (can be a subset sampled to run locally).
Pipeline Components
1. Batch ETL (bronze → silver → gold)
Bronze: land raw data (CSV, JSON, or as-is) immutably.
Silver: clean, type-cast, deduplicate, apply schema contracts (nullability, domains).
Gold: build analytics tables optimized for downstream queries. Apply partitioning and compaction strategies.
Evidence: EXPLAIN FORMATTED plans for silver→gold, Parquet footprint measurements.
2. Streaming Ingestion
Ingest a subset of your data through Structured Streaming (file source or socket).
Apply at least one windowed aggregation with watermark.
Write output in append mode to Parquet.
Evidence: query.lastProgress captured, Streaming UI screenshot.
You may reuse and improve your Lab 1 pipeline.
3. Text Processing
Build a text pipeline on a textual column/corpus from your track data.
Tokenize, normalize, remove stop-words, construct an inverted index or TF-IDF features.
Measure query latency and storage footprint (Parquet vs CSV).
Evidence: footprint comparison, query latency benchmarks.
You may reuse and improve your Lab 2 pipeline.
4. Iterative Workload (Graph or Clustering)
Graph option: build a graph, run iterative PageRank or connected components, analyze per-iteration shuffle costs and convergence.
Clustering option: prepare features, run KMeans/BisectingKMeans sweep, track silhouette scores and per-configuration costs.
Both: partitioning before/after comparison with metrics.
Evidence: per-iteration/per-configuration metrics, before/after plans, Spark UI screenshots.
You may reuse and improve your Lab 3 pipeline.
5. LLM Data Readiness
Prepare a curated text dataset suitable for LLM fine-tuning or RAG (Retrieval-Augmented Generation):
Extract and clean text fields into a structured format (doc_id, text, metadata).
Apply quality filters (minimum length, language detection, deduplication).
Export as Parquet with schema documentation.
Document the data card: source, size, schema, quality filters applied, intended use.
This is a data-engineering deliverable, thus, you do NOT run an LLM, you prepare the data pipeline for one.
Deliverables
Code: one primary notebook DE2_Project_Notebook_EN.ipynb plus helper scripts if desired.
Pipeline layout under outputs/project/:
bronze/ : raw landed data
silver/ : cleaned, typed, schema-contracted
gold/ : analytics tables, iterative workload outputs
streaming/ : streaming pipeline output (Parquet checkpoints)
text/ : inverted index or TF-IDF features
llm_ready/ : curated text dataset for LLM consumption
Proof in proof/: physical plans (.txt) for critical stages and Spark UI screenshots.
Metrics: project_metrics_log.csv with per-stage experiments (ETL, streaming, text, iterative, LLM prep).
Report: DE2_Project_Report.md (≤ 8 pages), concise and technical.
Config: de2_project_config.yml (paths, SLOs, pipeline params, keys).
Generative AI: project_genai.md : how you used generative AI (or state you did not).
Milestones
A. Design & Baseline (15%)
Problem statement with measurable SLOs (latency, footprint, quality thresholds).
Schema design with natural keys and schema contracts.
Bronze → silver → gold ETL pipeline working end-to-end.
Streaming ingestion pipeline delivering windowed aggregation to Parquet.
Baseline plans and metrics for each stage.
B. Hardening & Optimization (15%)
Text pipeline: inverted index or TF-IDF, footprint comparison, latency benchmarks.
Iterative workload: graph or clustering with partitioning optimization and before/after report.
LLM data readiness: curated dataset with data card and quality filters.
Layout optimization: compaction, partition tuning, exchange optimization across the full pipeline.
Measured gains for each optimization (before/after metrics).
SLO Examples
Streaming latency: end-to-end window aggregation ≤ 30s trigger interval.
Text query latency: inverted index lookup ≤ 2s for single-term query on full corpus.
Clustering quality: Silhouette ≥ 0.25 for best k.
Pipeline latency: full bronze→gold ≤ 10 min on laptop i7/16GB.
Storage: Parquet total size ≤ 60% of CSV baseline.
LLM data quality: ≥ 80% of documents pass quality filters (length, language, dedup).
Rules
Show paired evidence: plan and UI before/after each optimization.
Integrate Labs 1–3 work into the final pipeline (you may reuse and improve your lab code).
Use broadcast only when justified by cardinality.
State your iterative workload choice (graph or clustering) explicitly.
Team. Pair.





Data Engineering — ESIEE

Search




Explorer
DE2 Project Notebook EN
DE2_Final_Project_Brief_EN
DE2_Final_Project_Checklist_EN
DE2_Final_Project_Rubric_EN
DE2_Project_Report
Resources
Home
❯

DE2 — Data Engineering II
❯

project final
❯

DE2_Final_Project_Checklist_EN
DE2_Final_Project_Checklist_EN
Apr 20, 20262 min read

DE2 — Final Project Checklist
Author : Badr TAJINI - Data Engineering II (Data-Intensive Workloads) - ESIEE 2025-2026

Milestone A — Design & Baseline
 Dataset approved and profiled (row counts, column types, skew)
 de2_project_config.yml filled (paths, SLOs, pipeline params, keys)
 Problem statement with measurable SLOs documented
 Schema contracts defined (nullability, domains, types)
 Bronze landing complete (immutable raw data)
 Silver cleaning complete (types, null policy, dedup)
 Gold analytics tables built with partition strategy
 Streaming pipeline working: file/socket source → window + watermark → Parquet sink
 Baseline plans saved (ETL, streaming stages) + UI screenshots
 Baseline metrics recorded in project_metrics_log.csv
Milestone B — Hardening & Optimization
 Text pipeline: tokenization, normalization, inverted index or TF-IDF
 Text footprint comparison (CSV vs Parquet) recorded
 Text query latency benchmarked
 Iterative workload choice stated (graph or clustering)
 Iterative algorithm run with per-iteration/per-config metrics
 Partitioning before/after comparison done with measured gains
 LLM-ready dataset exported: doc_id, text, metadata in Parquet
 Data card written for LLM dataset (source, size, schema, filters, intended use)
 Layout optimization applied (compaction, partition tuning, exchange)
 Optimized plans saved + UI screenshots
 All metrics updated in project_metrics_log.csv with before/after entries
 Report completed (≤ 8 pages) with figures and tables
 project_genai.md created
 Zip uploaded to GitHub and Google Form submitted
Graph View


Table of Contents
DE2 — Final Project Checklist
Milestone A — Design & Baseline
Milestone B — Hardening & Optimization
Backlinks
DE2 — Data Engineering II
project final
Created with Quartz v4.5.2 © 2026

GitHub
Discord Community
DE2_Final_Project_Checklist_EN







DE2 — Final Project Notebook
Author : Badr TAJINI - Data Engineering II (Data-Intensive Workloads) - ESIEE 2025-2026

This is the primary executable artifact. Fill config, run the full pipeline (ETL → Streaming → Text → Iterative → LLM Prep), and record evidence.


. Load config
import yaml, pathlib, datetime, time, json
from pyspark.sql import SparkSession, functions as F, types as T

with open("de2_project_config.yml") as f:
    CFG = yaml.safe_load(f)

spark = SparkSession.builder.appName("de2-project").master("local[*]").getOrCreate()
print("Spark:", spark.version)
print("UI:", spark.sparkContext.uiWebUrl)
CFG
1. Bronze — landing raw data
raw_glob = CFG["paths"]["raw_csv_glob"]
bronze = CFG["paths"]["bronze"]
proof = CFG["paths"]["proof"]

df_raw = spark.read.option("header", "true").csv(raw_glob)
df_raw.write.mode("overwrite").csv(bronze)
print("Bronze written:", bronze)
2. Silver — cleaning, typing, feature engineering
silver = CFG["paths"]["silver"]

# TODO: Adapt to your dataset
df_silver = (df_raw
    .withColumn("metric", F.col("metric").cast("double"))
    .withColumn("date", F.to_date("date"))
    .dropna(subset=["metric", "date"]))

df_silver.write.mode("overwrite").parquet(silver)
print("Silver written:", silver)
3. Gold — analytics tables
gold = CFG["paths"]["gold"]
partition_by = CFG["layout"]["partition_by"]

# TODO: Build gold analytics tables
# gold_q1 = ...
# gold_q1.write.mode("overwrite").partitionBy(*partition_by).parquet(f"{gold}/q1")
print("Gold written:", gold)
4. Streaming Pipeline
Build a Structured Streaming ingestion pipeline: file source, watermark, windowed aggregation, Parquet sink. Capture query.lastProgress and Streaming UI.

# TODO: Define streaming schema and source
# stream_schema = T.StructType([...])
# landing = CFG["paths"].get("streaming_landing", "data/project/landing/")
# pathlib.Path(landing).mkdir(parents=True, exist_ok=True)

# TODO: readStream with watermark and window
# df_stream = (spark.readStream.schema(stream_schema)
#     .option("header", "true").option("maxFilesPerTrigger", 1)
#     .csv(landing))
# windowed = (df_stream
#     .withWatermark("event_time", CFG["streaming"]["watermark"])
#     .groupBy(F.window("event_time", CFG["streaming"]["window_duration"]), "key_col")
#     .agg(F.count("*").alias("count"), F.avg("metric").alias("avg_metric")))

# TODO: writeStream to Parquet
# pathlib.Path("outputs/project/streaming").mkdir(parents=True, exist_ok=True)
# query = (windowed.writeStream.format("parquet")
#     .outputMode("append")
#     .option("path", "outputs/project/streaming")
#     .option("checkpointLocation", "outputs/project/streaming_checkpoint")
#     .trigger(processingTime=CFG["streaming"]["trigger_interval"])
#     .start())
# query.awaitTermination(timeout=60)
# progress = query.lastProgress
# print(json.dumps(progress, indent=2))
# query.stop()
5. Text Pipeline — Corpus → Inverted Index → Query
Ingest text corpus, tokenize, build inverted index, measure query latency, compare storage formats.

# TODO: Load text corpus with explicit schema
# corpus = spark.read.schema(...).option("header", "true").csv(CFG["paths"]["text_corpus"])
# print(f"Documents: {corpus.count()}")

# TODO: Tokenize, normalize, remove stop-words
# tokens = (corpus
#     .withColumn("text_clean", F.regexp_replace(F.lower("text"), r"[^a-z0-9\\s]", ""))
#     .withColumn("tokens", F.split("text_clean", r"\\s+"))
#     .select("doc_id", F.explode("tokens").alias("token"))
#     .filter(F.length("token") > 0))

# TODO: Build inverted index
# inverted_index = (tokens.groupBy("token")
#     .agg(F.collect_list("doc_id").alias("doc_ids"), F.count("*").alias("freq"))
#     .orderBy(F.desc("df")))
# inverted_index.write.mode("overwrite").parquet("outputs/project/text")
# print(f"Unique terms: {inverted_index.count()}")

# TODO: Query latency measurement (≥3 terms)
# idx = spark.read.parquet("outputs/project/text")
# idx.cache(); idx.count()
# for term in CFG["text"]["query_terms"]:
#     t0 = time.time()
#     result = idx.filter(F.col("token") == term).collect()
#     print(f"'{term}': {(time.time()-t0)*1000:.1f} ms")
6. Iterative Workload — Graph OR Clustering
Choose one path. Graph: iterative PageRank with partitioning experiment. Clustering: KMeans/BisectingKMeans sweep with seed stability and drift.

# === Path A: Graph Processing ===
# TODO: Build vertex/edge DataFrames
# TODO: Iterative PageRank with per-iteration metrics
# TODO: Partitioning experiment (repartition edges)

# === Path B: Clustering ===
# TODO: Feature scaling + KMeans/BisectingKMeans sweep
# TODO: Seed stability (≥3 seeds, mean ± std of silhouette)
# TODO: Drift detection across time periods

# from pyspark.ml.feature import VectorAssembler, StandardScaler
# from pyspark.ml.clustering import KMeans, BisectingKMeans
# from pyspark.ml.evaluation import ClusteringEvaluator
# evaluator = ClusteringEvaluator(featuresCol="scaled_features", metricName="silhouette")
7. LLM Data Readiness
Prepare a curated dataset suitable for LLM consumption. Apply quality filters, enforce schema, document versioning strategy.

# TODO: Build curated dataset for LLM consumption
# Start from your silver/gold data and apply quality filters:
# - Remove nulls in text columns
# - Ensure UTF-8 encoding
# - Filter records with text length >= 100 chars
# - Deduplicate by content hash (xxhash64 or sha256)
# - Add metadata columns: source, version, timestamp, content_hash

# llm_rules = CFG.get("llm", {})
# df_llm = (spark.read.parquet(silver)
#     .filter(F.col("text").isNotNull())
#     .filter(F.length("text") >= llm_rules.get("min_text_length", 100))
#     .withColumn("content_hash", F.xxhash64("text"))
#     .dropDuplicates(["content_hash"])
#     .withColumn("source", F.lit(CFG["track"]))
#     .withColumn("version", F.lit("v1.0"))
#     .withColumn("curated_at", F.current_timestamp()))

# pathlib.Path("outputs/project/llm_ready").mkdir(parents=True, exist_ok=True)
# df_llm.write.mode("overwrite").parquet("outputs/project/llm_ready")
# print(f"LLM-ready records: {df_llm.count()}")
# df_llm.printSchema()
8. Evidence — Plans and Metrics
Save query plans for all critical stages. Record all measurements in project_metrics_log.csv. Capture Spark UI screenshots.

import os
pathlib.Path(proof).mkdir(parents=True, exist_ok=True)

# TODO: Save plans for critical stages:
# - proof/plan_etl.txt
# - proof/plan_streaming.txt + proof/query_progress.json
# - proof/plan_index_build.txt + proof/plan_query.txt
# - proof/plan_iterative.txt (graph or clustering)
# - proof/plan_llm_curation.txt

# TODO: Fill project_metrics_log.csv with columns:
# run_id, stage, task, metric_name, metric_value, notes, timestamp

# TODO: Capture Spark UI screenshots → proof/

print("Record plans, metrics, and Spark UI screenshots now.")

spark.stop()
print("Spark session stopped.")









Data Engineering — ESIEE

Search




Explorer
DE2 Project Notebook EN
DE2_Final_Project_Brief_EN
DE2_Final_Project_Checklist_EN
DE2_Final_Project_Rubric_EN
DE2_Project_Report
Resources
Home
❯

DE2 — Data Engineering II
❯

project final
❯

DE2_Final_Project_Rubric_EN
DE2_Final_Project_Rubric_EN
Apr 20, 20261 min read

DE2 — Final Project Rubric (30%)
Author : Badr TAJINI - Data Engineering II (Data-Intensive Workloads) - ESIEE 2025-2026

Area	Points	Evidence
Problem framing & SLOs	4	Clear use-case, measurable SLOs in config/report
Batch ETL pipeline (bronze→silver→gold)	5	Correct schemas, lineage, schema contracts, reproducible runs
Streaming ingestion (window, watermark, Parquet sink)	5	Working pipeline, query.lastProgress, Streaming UI screenshot
Text processing (index/TF-IDF, footprint, latency)	5	Inverted index or TF-IDF, query latency, CSV vs Parquet comparison
Iterative workload — graph or clustering (partitioning, convergence)	5	Per-iteration metrics, before/after, partitioning report
LLM data readiness + documentation	3	Curated dataset, data card, quality filters documented
Physical design & optimization (layout, compaction, exchange)	3	Before/after plans, measured gains, clear recommendations
Total	30	
IMPORTANT1: Spark UI metrics must be recorded in project_metrics_log.csv. Missing or inconsistent metrics will lead to a deduction.

IMPORTANT2: project_metrics_log.csv records each execution (run_id), the stage (ETL, streaming, text, iterative, llm_prep), any notes, and key metrics (shuffle, elapsed, quality scores). The objective is to keep a reproducible record of runs and have factual support for your claims.

IMPORTANT3: The project integrates all skills from Labs 1–3 plus LLM data readiness. Each lab’s topic must appear as a pipeline component. Reusing and improving lab code is encouraged.

Graph View

Backlinks
DE2 — Data Engineering II
project final
Created with Quartz v4.5.2 © 2026

GitHub
Discord Community
DE2_Final_Project_Rubric_EN










Data Engineering — ESIEE

Search




Explorer
DE2 Project Notebook EN
DE2_Final_Project_Brief_EN
DE2_Final_Project_Checklist_EN
DE2_Final_Project_Rubric_EN
DE2_Project_Report
Resources
Home
❯

DE2 — Data Engineering II
❯

project final
❯

DE2_Project_Report
DE2_Project_Report
Apr 20, 20262 min read

DE2 — Final Project Report
Author : Badr TAJINI - Data Engineering II (Data-Intensive Workloads) - ESIEE 2025-2026

1. Use-case and Dataset
Problem statement and target user.
Dataset origin, size, schema, known issues.
Track selected (A/B/C/D) and rationale.
2. System and SLOs
Hardware and Spark config (versions).
SLOs and acceptance thresholds.
Design choices and constraints.
3. Batch ETL Pipeline Design
Bronze (landing) design and schema contracts.
Silver (cleaning, typing, deduplication).
Gold (analytics tables, partition strategy).
Lineage diagram (ASCII or image).
4. Streaming Ingestion
Source type and schema.
Window and watermark configuration.
Output mode and Parquet sink.
Monitoring: query.lastProgress and Streaming UI evidence.
Gains vs SLOs (trigger latency, throughput).
5. Text Processing
Corpus description and preprocessing steps.
Inverted index or TF-IDF construction.
Query latency benchmarks.
Storage footprint: Parquet vs CSV comparison.
6. Iterative Workload (Graph or Clustering)
Choice and rationale (graph or clustering).
Algorithm and configuration.
Per-iteration/per-configuration metrics.
Convergence analysis (delta or silhouette curve).
Partitioning before/after comparison.
Skew analysis (graph) or stability analysis (clustering).
7. LLM Data Readiness
Text fields extracted and cleaned.
Quality filters applied (length, language, dedup).
Output schema: doc_id, text, metadata.
Data card: source, size, intended use.
8. Physical Design & Optimization
Partitioning, compaction, exchange strategies.
Before/after plans and UI evidence.
Metrics comparison table.
9. Results and Limits
Gains vs SLOs, failure modes, trade-offs.
Integration: how batch ETL → streaming → text → iterative → LLM data form a coherent pipeline.
Future work.
≤ 8 pages. Keep prose compact and technical.

Graph View


Table of Contents
DE2 — Final Project Report
1. Use-case and Dataset
2. System and SLOs
3. Batch ETL Pipeline Design
4. Streaming Ingestion
5. Text Processing
6. Iterative Workload (Graph or Clustering)
7. LLM Data Readiness
8. Physical Design & Optimization
9. Results and Limits
Created with Quartz v4.5.2 © 2026

GitHub
Discord Community
DE2_Project_Report














Data Engineering — ESIEE

Search




Explorer
DE2 Project Notebook EN
DE2_Final_Project_Brief_EN
DE2_Final_Project_Checklist_EN
DE2_Final_Project_Rubric_EN
DE2_Project_Report
roadmap-labs-project-DE2
roadmap-labs-project-DE2-FR
Resources
Home
❯

DE2 — Data Engineering II
❯

roadmap
❯

roadmap labs project DE2 FR
roadmap-labs-project-DE2-FR
Apr 22, 20266 min read

Data Engineering II (Charges data-intensives) — Labs & Projet
Author : Badr TAJINI

Année académique : 2025–2026
Ecole : ESIEE Paris
Cours : Data Engineering II (Charges data-intensives)

1. Objectifs du cours
Concevoir et instrumenter des pipelines streaming (Structured Streaming, fenêtres, watermarks, sinks Parquet) et mesurer la latence et le débit.
Construire des pipelines de traitement de texte (tokenisation, index inversé, TF-IDF) et mesurer les coûts d’I/O, la latence de requête et l’empreinte de stockage.
Implémenter et évaluer des charges itératives : soit en traitement de graphes (PageRank, connected components), soit en clustering (KMeans, BisectingKMeans) : avec une attention particulière au partitionnement, aux coûts de shuffle et à la convergence.
Préparer une infrastructure de données pour les LLMs du point de vue plateforme : curation, filtres qualité, design de schéma, versionnage.
Appliquer une optimisation fondée sur des preuves : explain("formatted"), Spark UI, journaux de métriques, comparaisons avant / après.
2. Compétences acquises
Associer des charges data-intensives (streaming, texte, graphes, clustering) à des représentations et layouts adaptés.
Instrumenter chaque étape avec explain("formatted"), Spark UI et journaux de métriques.
Mesurer et comparer les coûts (shuffle, I/O, spill) avant et après optimisation, avec des preuves quantitatives.
Proposer des améliorations défendables alignées avec des SLO mesurables.
3. Prérequis
Validation de Data Engineering I (ETL, plans Spark, Parquet, métriques).
Python et SQL de base.
Familiarité avec le terminal, Git et conda.
4. Contenu du cours (6 chapitres)
Text Processing I : ingestion de texte, normalisation, tokenisation, index inversé, représentations vectorielles creuses, pondération.
Text Processing II : représentations denses, top-k retrieval, rerankers, RAG, MCP, relation sparse / dense.
Finding Similar Items : collisions de hachage, MinHash, LSH, random projections, clustering (KMeans, GMM), banding.
Graph Processing : représentations de graphes, algorithmes (PageRank, BFS), edge partitioning, coûts de communication, skew.
Stream Processing : micro-batch vs continu, fenêtres, watermarks, sémantiques de livraison, tolérance aux pannes, intégration lakehouse.
LLMs & infrastructure data : curation des données, tables de features, fraîcheur, versionnage, gouvernance ; angle plateforme, pas angle algorithmes.
5. Techniques et méthodes
Mesure systématique : explain("formatted"), Spark UI (Files Read, Input Size, Shuffle Read/Write, Spill).
Comparaisons avant / après : même seed, même échantillon, mêmes conditions.
Contrats de schéma à l’ingestion, conversion colonnaire, partitionnement guidé par l’usage.
Reproductibilité locale : conda, Java 21, Spark 4, notebooks scriptables, seeds fixes.
Journal d’expérience : CHANGELOG.md, EXPERIMENTS.md, PLAN_EVIDENCE.md.
6. Outils techniques
Installation locale : conda (Python 3.10), OpenJDK 21, Maven, JupyterLab.
Spark : Spark 4.0.0 précompilé ; PySpark dans Jupyter et via spark-submit.
MLlib : KMeans, BisectingKMeans, ClusteringEvaluator, VectorAssembler (clustering uniquement ; pas de ML supervisé).
Structured Streaming : micro-batch, sinks fichier / console, watermarks, trigger intervals.
GraphFrames (optionnel) : pour les algorithmes de graphe ; ou joins itératifs manuels.
Vérification : session Spark, lecture CSV / Parquet, comparaison de plans, captures Spark UI.
7. Acquis d’apprentissage
À l’issue du cours, l’étudiant est capable de :

Construire des pipelines data-intensifs (streaming, texte, graphes / clustering) et produire des plans et métriques comme preuves.
Expliquer les trade-offs d’architecture pour chaque type de charge et défendre ses choix par des mesures.
Documenter la reproductibilité, la traçabilité et la qualité de ses pipelines.
8. Évaluation
Labs : 40 %
Lab 1 (10 %) : Streaming : pipeline Structured Streaming, fenêtres, watermarks, sink Parquet, monitoring, optimisation avant / après
Lab 2 (15 %) : Traitement de texte : ingestion de corpus, normalisation, index inversé, latence de requête, empreinte disque (CSV vs Parquet)
Lab 3 (15 %) : Charge itérative (Graphes OU Clustering) : stratégies de partitionnement, métriques par itération, convergence, analyse du skew, rapport avant / après
Projet final : 30 %
Partie A (15 %) : pipeline end-to-end (batch ETL + streaming), SLO, contrats de schéma, plans et métriques de base
Partie B (15 %) : pipeline texte, charge itérative, préparation LLM, optimisation de layout, rapport + preuves
Documentation (rapports et preuves) : 20 %
Participation et Q&A : 10 %
Lab 0 — Bootstrap (non noté)
Revalider l’environnement local, tester PySpark, lire le plan du cours et collecter les premières métriques. Sert de point de départ pour les labs suivants.

Labs notés (trois niveaux progressifs)
Lab 1 : pipeline Structured Streaming avec source fichier / socket, agrégation fenêtrée, watermarks, sink Parquet, query.lastProgress, Streaming UI, optimisation avant / après.
Lab 2 : traitement de texte : ingestion de corpus, tokenisation, normalisation, suppression de stop words, construction d’un index inversé, mesure de latence, comparaison d’empreinte Parquet vs CSV.
Lab 3 : charge itérative : au choix graph processing (PageRank via joins itératifs ou GraphFrames) OU clustering (sweep KMeans / BisectingKMeans). Dans les deux cas : partitionnement, métriques par itération, convergence, rapport avant / après.
Projet final (deux parties)
Partie A : pipeline end-to-end, batch ETL (bronze → silver → gold), ingestion streaming, SLO, calibrations de base, preuves par plans et métriques.
Partie B : pipeline texte, charge itérative (graphes ou clustering), préparation de données pour LLMs, optimisation du layout (compaction, partitionnement), rapport ≤ 8 pages.
4 pistes thématiques
Au choix une piste et vous la conservez pour les Labs 1–3 et le projet :

Track A — Esport (OpenDota) : matchs, héros, archétypes, impact des patches
Track B — Open Source (GitHub Archive) : événements, PR, rythmes de release
Track C — Micromobilité (Citi Bike) : trajets, stations, stock-out, résilience
Track D — Aviation (OpenSky) : segments de vol, aéroports, régimes d’espace aérien
9. Références
Ouvrages : Designing Data-Intensive Applications (2nd ed.) ; Fundamentals of Data Engineering ; Mining of Massive Datasets (chap. 3, 5).
Technique : documentation PySpark, Spark MLlib, guide Structured Streaming.
Recherche d’information texte : Data-Intensive Text Processing with MapReduce (chap. 4–5) ; Pretrained Transformers for Text Ranking.
Streaming : Apache Beam : Streaming 101 & 102 ; Kafka Streams in Action (chap. 1–2).
Graphes : Scale Up or Scale Out for Graph Processing? ; article COST (McSherry et al.).
Datasets : OpenDota, GitHub Archive, Citi Bike, OpenSky, Wikipedia Clickstream, Open Food Facts.
Livrables
Notebooks propres et exécutables
Captures Spark UI
Tableaux de métriques avant / après
Rapports concis et traçables (hypothèses, choix, preuves, limites, recommandations)
GENAI.md déclarant l’usage éventuel d’IA générative
Graph View


Table of Contents
Data Engineering II (Charges data-intensives) — Labs & Projet
1. Objectifs du cours
2. Compétences acquises
3. Prérequis
4. Contenu du cours (6 chapitres)
5. Techniques et méthodes
6. Outils techniques
7. Acquis d’apprentissage
8. Évaluation
Lab 0 — Bootstrap (non noté)
Labs notés (trois niveaux progressifs)
Projet final (deux parties)
4 pistes thématiques
9. Références
Livrables
Created with Quartz v4.5.2 © 2026

GitHub
Discord Community
roadmap-labs-project-DE2-FR