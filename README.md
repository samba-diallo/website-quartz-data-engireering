# Data Engineering — ESIEE Paris

> **Author** : Badr TAJINI — Data Engineering I & II — ESIEE Paris 2025-2026
>
> **Students** : DIALLO Samba & DIOP Mouhamed

🌐 **Site de documentation** → https://website-quartz-data-engireering.pages.dev/Data-Engineering-2
📊 **Dashboard temps réel (Projet Final DE2)** → https://de2-dashboard-e2e.pages.dev/

[![Quartz](https://img.shields.io/badge/Built%20with-Quartz-blue)](https://quartz.jzhao.xyz/)
[![Spark](https://img.shields.io/badge/Apache-Spark%204.0-orange)](https://spark.apache.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)

---

## Vue d'ensemble

Ce repository regroupe les travaux pratiques et projets des cours **Data Engineering I & II** à ESIEE Paris, encadrés par le professeur **Badr TAJINI**. Il va des fondamentaux du traitement distribué avec **Apache Spark** (DE1) jusqu'à un **pipeline d'analytics temps réel complet**, conteneurisé et déployé (DE2).

L'ensemble est documenté sur un **site statique généré avec Quartz**, déployé automatiquement sur Cloudflare Pages.

---

## Objectifs des projets

### Data Engineering I — Fondamentaux Spark
- API RDD vs DataFrame, Spark SQL & Catalyst Optimizer
- Stratégies de jointures (Broadcast, Sort-Merge), partitionnement, cache
- **Projet final** : pipeline ETL multi-sources optimisé (comparaison baseline vs optimisé)

### Data Engineering II — Workloads intensifs
- **Structured Streaming** : fenêtrage, watermarks, sémantique exactly-once
- **Index inversé distribué** & recherche full-text (TF-IDF)
- **Workloads itératifs ML** : clustering KMeans (convergence, stabilité, partitionnement)
- **Projet final** : pipeline temps réel de bout en bout sur le dataset *GitHub Archive* (détaillé ci-dessous)

---

## Architecture — Projet Final DE2

Pipeline **event-driven** suivant une **architecture Medallion**, orchestré en Docker Compose.

```
┌──────────────┐   ┌──────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────┐
│ GH Archive   │──▶│ Producer │──▶│ Kafka topic  │──▶│  Spark   │──▶│ Bronze   │
│  (.json.gz)  │   │ (Python) │   │ raw.events   │   │ Streaming│   │ Parquet  │
└──────────────┘   └──────────┘   └──────────────┘   └──────────┘   └────┬─────┘
                                                                          │
                          ┌──────────┐   ┌──────────┐   ┌─────────────────┘
                          │ Frontend │◀──│  FastAPI │◀──│ Gold / Silver
                          │ Next.js  │   │ + DuckDB │   │ (Airflow DAG)
                          └──────────┘   └──────────┘   └─────────────────
```

- **Bronze** : événements bruts du topic Kafka (Spark Structured Streaming → Parquet)
- **Silver** : événements nettoyés et normalisés (batch Airflow)
- **Gold** : agrégations applicatives — `repo_activity`, `pagerank`, `user_activity`

Le tout est exposé via une **API FastAPI + DuckDB** et visualisé par un **dashboard Next.js temps réel**.

| Service | Rôle | Port |
|---|---|---|
| Kafka + Zookeeper | Bus de streaming (`github.raw.events`) | 9092 |
| Kafka UI | Inspection des topics | 8090 |
| Producer (Python) | Ingestion GitHub Archive → Kafka | — |
| Spark Streaming | Kafka → Parquet (Bronze), 24/7 | — |
| Airflow (web + scheduler) | Orchestration batch Silver/Gold | 8080 |
| Postgres | Metadata Airflow | — |
| FastAPI + DuckDB | API analytics (lit la couche Gold) | 8000 |
| Next.js dashboard | Visualisation temps réel | 3000 |

---

## Structure du repository

```
Data Engineering/
├── Data Engineering 1/          # Fondamentaux Spark (labs + projet final)
├── Data Engineering 2/          # Workloads intensifs
│   └── project final/           # Pipeline E2E temps réel
│       ├── kafka/  spark/  airflow/  backend/  frontend-dashboard/
│       └── docker-compose.yml   # Orchestration des 10 services
├── content/                     # Sources du site Quartz
├── quartz/                      # Moteur Quartz
├── tools/                       # Scripts de génération du site
├── documentation/               # PIPELINE_RUNBOOK.md
└── .github/workflows/           # CI/CD (build, deploy, dashboard CI)
```

---

## Stack technique

- **Big Data** : Apache Spark 4 / PySpark · Structured Streaming · Parquet · DuckDB
- **Streaming & orchestration** : Apache Kafka (Confluent) · Apache Airflow · Postgres
- **Backend / Frontend** : FastAPI · Next.js 16 + Tailwind v4 + Recharts + Framer Motion
- **Machine Learning** : Spark MLlib (KMeans, BisectingKMeans)
- **Infra & CI/CD** : Docker Compose · GitHub Actions · Cloudflare Pages
- **Documentation** : Quartz (static site generator) · Markdown · Mermaid

---

## Lancer le projet

### A. Labs Spark (notebooks DE1 & DE2)
Prérequis : Java 11/17, Python 3.10+, Spark 4.0.1.
```bash
pip install pyspark
jupyter notebook        # ou ouvrir les .ipynb dans VS Code
```

### B. Projet Final DE2 (pipeline complet)
Prérequis : Docker + Docker Compose.
```bash
cd "Data Engineering 2/project final"
cp .env.example .env          # renseigner les valeurs <change_me>
docker compose up -d
```
Accès : dashboard `http://localhost:3000` · API `http://localhost:8000/docs` · Airflow `http://localhost:8080` · Kafka UI `http://localhost:8090`

→ Guide complet : **[documentation/PIPELINE_RUNBOOK.md](documentation/PIPELINE_RUNBOOK.md)** (configuration, vérifications, troubleshooting, arrêt propre).

### C. Site Quartz (local)
Prérequis : Node.js 22+.
```bash
npm install
npx quartz build --serve      # http://localhost:8080
```

---

## Sécurité & qualité

- Credentials externalisés via `.env` (jamais commités) ; template `.env.example` fourni.
- CI GitHub Actions : build Quartz + scan de secrets (gitleaks) + CodeQL.
- Branche `main` protégée (PR + CI requis) ; déploiement auto Cloudflare Pages.

---

## Licence

Projet académique réalisé à ESIEE Paris (2025-2026) sous l'encadrement du professeur **Badr TAJINI**.

© 2025-2026 — DIALLO Samba & DIOP Mouhamed.
