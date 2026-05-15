# Intégration Kafka + Airflow — GitHub Archive Platform

> **Contexte** : Le projet final actuel (DE2) est ~90% terminé avec PySpark + DuckDB + FastAPI + Next.js.
> Cette feuille de route décrit comment **évoluer vers la v2** en intégrant Kafka et Airflow
> pour en faire un vrai projet portfolio "production-grade".

---

## 🗺️ Vision : De l'actuel vers la cible

```
# ÉTAT ACTUEL (v1 — terminée ✅)
GH Archive (.json.gz local)
    ↓ [Script Python]
PySpark Batch (local[*])
    ↓
Bronze / Silver / Gold (Parquet)
    ↓
DuckDB → FastAPI → Next.js

# CIBLE (v2 — avec Kafka + Airflow)
GH Archive (API horaire)
    ↓ [Producer Python]
Kafka (topic: github.raw.events)
    ↓ [Spark Structured Streaming]
Bronze Layer (Delta Lake)
    ↓ [Spark Batch — déclenché par Airflow DAG]
Silver → Gold (Delta Lake)
    ↓ [dbt run — déclenché par Airflow DAG]
PostgreSQL / DuckDB
    ↓
FastAPI → Next.js Dashboard
```

---

## 🏗️ Architecture Cible Complète

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATION LAYER                             │
│                    Apache Airflow (port 8080)                           │
│   ┌────────────────────────────────────────────────────────┐            │
│   │  DAG: gh_archive_pipeline                              │            │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │            │
│   │  │ Task 1   │→│ Task 2   │→│ Task 3   │→│ Task 4   │  │            │
│   │  │ Ingest   │ │ Spark    │ │ dbt run  │ │ Validate │  │            │
│   │  │ Producer │ │ Batch    │ │          │ │ SLOs     │  │            │
│   │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │            │
│   └────────────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
                    │ déclenche
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         STREAMING LAYER                                 │
│                                                                         │
│   GitHub Archive API ──→ Producer Python ──→ Kafka (topic: gh.events)  │
│                                                         │               │
│                              Spark Structured Streaming ←┘              │
│                                       │                                 │
│                              Bronze (Delta Lake)                        │
└─────────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         TRANSFORMATION LAYER                            │
│                                                                         │
│   Bronze → [Spark Batch] → Silver → [Spark Batch] → Gold               │
│                                                   ↓                     │
│                               [dbt] → PostgreSQL (marts analytiques)   │
└─────────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         SERVING LAYER                                   │
│   DuckDB (Parquet) + PostgreSQL → FastAPI → Next.js Dashboard           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Rôle de chaque outil

### Apache Kafka
**Ce qu'il remplace** : Le script `simulate_streaming.py` qui écrit des fichiers locaux.

**Ce qu'il apporte** :
- **Découplage** : le producteur (téléchargement GH Archive) et le consommateur (Spark) sont indépendants
- **Rejeu** : les messages Kafka sont persistés → tu peux re-processer sans retélécharger
- **Scalabilité** : tu peux avoir plusieurs consommateurs (Spark Streaming + monitoring)
- **Vrai temps réel** : latence end-to-end de quelques secondes

**Topics à créer** :
| Topic | Contenu | Partitions | Retention |
|-------|---------|-----------|-----------|
| `github.raw.events` | Événements bruts JSON | 3 | 24h |
| `github.push.events` | PushEvent filtrés | 2 | 48h |
| `github.pr.events` | PullRequestEvent filtrés | 2 | 48h |
| `github.dlq` | Dead Letter Queue (erreurs parsing) | 1 | 7j |

### Apache Airflow
**Ce qu'il remplace** : Le lancement manuel des scripts / notebooks.

**Ce qu'il apporte** :
- **Scheduling** : pipeline batch toutes les heures, automatiquement
- **Dependencies** : Silver ne tourne que si Bronze est validé
- **Monitoring** : interface web avec historique, logs, alertes
- **Retry** : relance automatique en cas d'échec

**DAGs à créer** :
| DAG | Schedule | Description |
|-----|---------|-------------|
| `gh_archive_streaming_producer` | `@hourly` | Lance le Producer Python → Kafka |
| `gh_archive_batch_pipeline` | `@hourly` | Bronze→Silver→Gold via Spark |
| `dbt_analytics_run` | `@hourly` (après batch) | Transformations dbt → PostgreSQL |
| `slo_validation` | `@daily` | Vérifie les SLOs et génère un rapport |

---

## 📦 Structure du projet v2

```
github-archive-platform/          ← Nouveau repo (ou branche v2)
│
├── airflow/
│   ├── dags/
│   │   ├── gh_archive_producer.py
│   │   ├── gh_archive_batch.py
│   │   ├── dbt_run.py
│   │   └── slo_validation.py
│   ├── plugins/
│   └── Dockerfile
│
├── kafka/
│   ├── producer/
│   │   ├── gh_producer.py         ← Télécharge GH Archive → envoie dans Kafka
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── config/
│       └── topics.yml
│
├── spark/
│   ├── streaming/
│   │   └── bronze_consumer.py     ← Kafka → Bronze (Delta)
│   ├── batch/
│   │   ├── silver_transformer.py  ← Bronze → Silver
│   │   └── gold_aggregator.py     ← Silver → Gold
│   └── Dockerfile
│
├── dbt/
│   ├── models/
│   │   ├── staging/               ← lectures Gold Parquet
│   │   ├── marts/                 ← top_repos, event_distribution, pagerank
│   │   └── metrics/               ← SLOs, KPIs
│   ├── profiles.yml
│   └── dbt_project.yml
│
├── backend/                       ← FastAPI (existant, légère évolution)
├── frontend-dashboard/            ← Next.js (existant)
├── infrastructure/
│   └── docker-compose.yml         ← Nouveau compose unifié
└── scripts/
    └── init_topics.sh             ← Crée les topics Kafka au démarrage
```

---

## 🚀 Plan d'intégration — Phases progressives

### Phase 1 — Kafka MVP (1-2 jours) 🔥 *Commencer ici*

**Objectif** : Remplacer `simulate_streaming.py` par un vrai Producer Kafka.

**Ce à faire** :
1. Ajouter Kafka + Zookeeper au `docker-compose.yml`
2. Écrire `kafka/producer/gh_producer.py` :
   - télécharge un fichier GH Archive horaire
   - parse ligne par ligne
   - envoie chaque événement JSON dans `github.raw.events`
   - supprime le fichier temporaire
3. Modifier `spark/streaming/bronze_consumer.py` :
   - lire depuis Kafka (pas depuis `data/landing/`)
   - écrire en Delta Lake (pas en Parquet basique)
4. Valider : messages visibles dans Kafka UI

**Docker Compose à ajouter** :
```yaml
zookeeper:
  image: confluentinc/cp-zookeeper:7.5.0
  environment:
    ZOOKEEPER_CLIENT_PORT: 2181

kafka:
  image: confluentinc/cp-kafka:7.5.0
  depends_on: [zookeeper]
  ports:
    - "9092:9092"
  environment:
    KAFKA_BROKER_ID: 1
    KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
    KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

kafka-ui:
  image: provectuslabs/kafka-ui:latest
  ports:
    - "8090:8080"
  environment:
    KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:29092
```

---

### Phase 2 — Airflow MVP (2-3 jours)

**Objectif** : Orchestrer le pipeline batch Bronze→Silver→Gold.

**Ce à faire** :
1. Ajouter Airflow au `docker-compose.yml` (image `apache/airflow:2.8.0`)
2. Créer le DAG `gh_archive_batch.py` :
   ```python
   with DAG("gh_archive_batch", schedule="@hourly") as dag:
       t1 = BashOperator(task_id="spark_silver", bash_command="spark-submit silver_transformer.py")
       t2 = BashOperator(task_id="spark_gold", bash_command="spark-submit gold_aggregator.py")
       t1 >> t2
   ```
3. Créer le DAG `gh_archive_producer.py` qui déclenche le Producer Kafka
4. Valider : pipeline complet visible dans Airflow UI

---

### Phase 3 — dbt + PostgreSQL (2-3 jours)

**Objectif** : Couche analytics propre et testée.

**Ce à faire** :
1. Ajouter PostgreSQL au `docker-compose.yml`
2. Créer les modèles dbt :
   - `staging/stg_repo_activity.sql` (lecture Gold Parquet via DuckDB)
   - `marts/mart_top_repos.sql`
   - `marts/mart_event_distribution.sql`
3. Connecter FastAPI à PostgreSQL (en plus de DuckDB)
4. Brancher Airflow : `BashOperator(bash_command="dbt run")`

---

### Phase 4 — Delta Lake (1-2 jours)

**Objectif** : Remplacer Parquet basique par Delta Lake.

**Ce à faire** :
1. Ajouter `delta-spark` aux dépendances Spark
2. Modifier les writers Spark : `format("delta")` au lieu de `format("parquet")`
3. Activer le **compaction** automatique : `OPTIMIZE` et `VACUUM`
4. Activer le **schema enforcement** et le **Change Data Feed**

---

### Phase 5 — Polish & Portfolio (1 jour)

- Ajouter GitHub Actions CI pour tester les DAGs Airflow
- Documenter l'architecture dans Quartz
- Ajouter des screenshots dans le README
- Déployer le dashboard sur Cloudflare Pages

---

## ⚡ Comment intégrer SANS casser le projet actuel

> **Stratégie recommandée** : Créer une branche `v2-kafka-airflow` et garder `main` stable pour la soutenance.

```bash
# Dans ton repo actuel
git checkout -b v2-kafka-airflow

# Garder le projet actuel intact sur main
# Développer la v2 sur la nouvelle branche
```

Le projet actuel devient la **"v1 — Pipeline Batch Spark"** et la v2 devient la **"v2 — Streaming Platform Kafka + Airflow"**.

**Sur ton GitHub README**, tu peux montrer les deux versions comme une évolution naturelle :
> "v1: Pipeline batch PySpark → v2: Streaming Kafka + Orchestration Airflow"

C'est exactement ce qu'un recruteur Data Engineering veut voir : **tu sais faire évoluer une architecture**.

---

## 🎯 Priorisation pour le portfolio

| Outil | Impact Portfolio | Difficulté | À faire en priorité ? |
|-------|-----------------|-----------|----------------------|
| Kafka | ⭐⭐⭐⭐⭐ | Moyenne | ✅ **OUI — Phase 1** |
| Airflow | ⭐⭐⭐⭐⭐ | Moyenne | ✅ **OUI — Phase 2** |
| Delta Lake | ⭐⭐⭐⭐ | Facile | ✅ Oui (Phase 4) |
| dbt | ⭐⭐⭐⭐ | Facile | 🟡 Si temps |
| PostgreSQL | ⭐⭐⭐ | Facile | 🟡 Si temps |
| GitHub Actions | ⭐⭐⭐ | Facile | 🟡 Si temps |

**Kafka + Airflow sont les deux ajouts qui feront la plus grande différence** sur un CV Data Engineering.
