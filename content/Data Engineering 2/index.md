---
date: 2026-05-11
description: Cours DE2 - Lakehouse, Delta Lake, Streaming, Graphes, LLM-readiness
tags:
- lakehouse
title: Data Engineering 2
---

# Data Engineering 2

Cours **Data Engineering II** — *Data-Intensive Workloads* (ESIEE 2025-2026).
Pile technique : **Apache Spark 4.x (PySpark)**, **Delta Lake**, **Parquet**, **GitHub Archive** (Track B), **Kafka**, **Airflow**, **FastAPI**, **Next.js**.

> **Pour le correcteur** — cette page donne un aperçu de chaque rendu *avant* d'ouvrir le détail. Chaque carte ci-dessous résume l'objectif du lab, les livrables et pointe vers le notebook ainsi que les preuves d'exécution.

## Aperçu des labs

| Lab | Sujet | Practice | Assignment |
|---|---|---|---|
| 0 | Setup Spark + environnement | [[lab0 setup practice/index\|Setup practice]] | — |
| 1 | Streaming structuré + watermark | [[lab1 practice/index\|Practice]] | [[lab1 assignment/index\|Assignment]] |
| 2 | Traitement de texte (Inverted Index) | [[lab2 practice/index\|Practice]] | [[lab2 assignment/index\|Assignment]] |
| 3 | Charge itérative (Graphe / PageRank) | [[lab3 practice/index\|Practice]] | [[lab3 assignment/index\|Assignment]] |

### Lab 0 — Setup practice
Mise en place de l'environnement local : Spark 4.x en `local[*]`, Python 3.10, écriture/lecture Parquet, premier notebook de vérification.
→ [[lab0 setup practice/index|Ouvrir le lab 0]]

### Lab 1 — Streaming Pipeline (Track B)
Pipeline **Spark Structured Streaming** sur GitHub Archive : fenêtre 1 h, watermark 15 min, agrégations `count / countDistinct / sum`, sink Parquet.
Comparaison **baseline vs optimisé** (repartition par `event_type + repo_name`) avec plans d'exécution `EXPLAIN FORMATTED` et `lab1_metrics_log.csv`.
→ [[lab1 assignment/index|Voir l'assignment 1]]

### Lab 2 — Inverted Index (Texte)
Construction d'un **index inversé** à partir d'événements GitHub (PushEvent, IssuesEvent…) : tokenisation, stop-words, agrégation `token → [doc_ids]`.
Comparaison **Parquet vs CSV** sur la latence de lookup et l'empreinte disque, plans `plan_index_build.txt` et `plan_query.txt`.
→ [[lab2 assignment/index|Voir l'assignment 2]]

### Lab 3 — Charge itérative
Algorithme itératif distribué (graphe **PageRank** / connected components) avec mesure des coûts de **shuffle** par itération, analyse de convergence et expérience de partitionnement.
Sert de base au volet « graphe » du projet final.
→ [[lab3 assignment/index|Voir l'assignment 3]]

---

## Projet final — Pipeline GitHub Archive de bout en bout

**Track B — GitHub Archive** : pipeline data-intensive complet, du JSON brut horaire jusqu'à un dashboard temps réel déployé.

> ### 🎥 Vidéo de démonstration
> **▶ [Regarder la démo complète sur SharePoint ESIEE][demo-video]**
> Vue d'ensemble du pipeline et démonstration du dashboard en action.

> ### Démo en ligne
> **▶ Dashboard live :** https://de2-dashboard-e2e.pages.dev/
> Frontend **Next.js** déployé sur Cloudflare Pages, branché sur l'API analytics **FastAPI** du pipeline. Captures dans la [[project final/proof/|galerie de preuves]].

### Ce que contient le projet

1. **Architecture Medallion (Bronze / Silver / Gold)**
   Ingestion JSON brut → schéma aplati avec sélection précoce des colonnes (évite l'`OutOfMemoryError` sur le `payload` imbriqué) → table analytique `repo_activity` partitionnée par date.
2. **Streaming fichier**
   `FileStreamSource` avec `maxFilesPerTrigger=1`, fenêtre 5 min, watermark 10 min, sink Parquet en mode `append`.
3. **Traitement de texte**
   Index inversé sur les messages de commit (PushEvent) avec normalisation, stop-words et lookup `≤ 2 s` par terme.
4. **Charge itérative — PageRank**
   Graphe bipartite `actor_login → repo_name` (contributions Push/PR/Issues), PageRank par jointures distribuées (`damping = 0.85`), expérience de partitionnement par hash pour réduire les *Exchange*, courbe de convergence.
5. **LLM-readiness**
   Corpus filtré (longueur ≥ 50, déduplication par `xxhash64`) prêt pour fine-tuning ou RAG, documenté dans la **Data Card**.
6. **Extension Plateforme E2E (v2)** — au-delà du périmètre noté
   **Kafka** (ingestion event-driven) + **Airflow** (orchestration des DAGs Bronze/Silver/Gold) + **FastAPI** (API analytics DuckDB) + **Next.js** (dashboard temps réel). Le tout orchestré via **Docker Compose** et déployable en production.

### Deux faces, deux entrées

- **Rapport noté** → [[project final/Rapport_Projet|Rapport Final (Architecture, Batch, Streaming, Graphe)]] — version évaluée par le cours (SLOs, plans d'exécution, métriques).
- **Extension E2E** → [[project final/E2E_Plateforme|Plateforme E2E (Kafka + Airflow + FastAPI + Next.js)]] — au-dessus du pipeline noté.

### Sommaire détaillé du projet

1. [[project final/Rapport_Projet|Rapport final]] — la version notée
2. [[project final/E2E_Plateforme|Plateforme E2E (extension v2)]]
3. [[project final/Data_Card|Data Card]] — qualité des données pour l'IA
4. [[project final/Usage_IA|Déclaration d'utilisation de l'IA]]
5. [[project final/DE2_Project_Notebook_EN|Code source du notebook PySpark]]
6. [[project final/proof/|Preuves d'exécution]] — dashboard, Spark UI, plans, PageRank

→ **[[project final/index|Ouvrir la page du projet final]]**

---

## Support

[[support/index|Setup et troubleshooting]] — installation, problèmes courants, environnement.

*Roadmap officielle :* `roadmap-labs-project-DE2-FR.pdf` *(racine du dossier)*

[demo-video]: https://esieeparis-my.sharepoint.com/:v:/g/personal/samba_diallo_edu_esiee_fr/IQBddKK1juBnR5rsKe7DkHvjAZtsVvf1kMWr7NtC9Q4RpH8?e=FLKjyg&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D
