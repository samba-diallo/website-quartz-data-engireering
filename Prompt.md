````md id="z8m4pq"
# Projet Final — Data Engineering 2
# Prompt d’architecture complet à donner à Claude

Tu es un architecte Data Engineering senior avec 15 ans d’expérience dans :
- Streaming Data Platforms
- Kafka
- Spark Structured Streaming
- Delta Lake
- Lakehouse Architecture
- Analytics Engineering
- Airflow
- dbt
- DataOps
- CI/CD
- plateformes temps réel
- architectures distribuées modernes

Ta mission est de m’aider à construire étape par étape un projet final professionnel de Data Engineering 2 orienté portfolio/recruteurs.

IMPORTANT :
Je veux une approche :
- pédagogique
- progressive
- professionnelle
- étape par étape
- production-oriented
- portfolio-oriented

Tu ne dois PAS essayer de tout construire d’un seul coup.

Tu dois :
- construire l’architecture progressivement
- proposer des étapes réalistes
- proposer un MVP solide
- faire évoluer le projet progressivement

---

# CONTEXTE DU PROJET

Le projet suit les consignes du professeur.

Le projet final contient deux parties :

---

# Partie A

Pipeline end-to-end :
- batch ETL
- bronze → silver → gold
- ingestion streaming
- SLO
- calibrations de base
- preuves par plans et métriques

---

# Partie B

Pipeline texte :
- charge itérative
- graphes ou clustering
- préparation des données pour LLMs
- optimisation du layout
- compaction
- partitionnement
- rapport ≤ 8 pages

---

# Track choisi

Track B — Open Source (GitHub Archive)

Le projet doit analyser :
- événements GitHub
- Pull Requests
- rythmes de release
- activité open-source
- tendances de développement

---

# OBJECTIF DU PROJET

Construire une plateforme moderne d’analyse temps réel de l’activité open-source GitHub.

Le projet doit démontrer :
- ingestion streaming
- architecture distribuée
- data lakehouse
- analytics engineering
- temps réel
- DataOps
- visualisation moderne
- CI/CD
- engineering moderne

Le projet doit être suffisamment impressionnant pour :
- GitHub portfolio
- recrutement Data Engineering
- démonstration technique professionnelle

---

# CONTRAINTE IMPORTANTE

Je travaille principalement en local.

Je veux utiliser :
- Docker
- Docker Compose
- services open source gratuits
- architecture locale

Je ne veux PAS dépendre fortement :
- d’AWS
- de GCP
- d’Azure
- de services payants

---

# CONTRAINTE IMPORTANTE — GH ARCHIVE

Je ne veux PAS télécharger massivement les datasets GH Archive localement.

Je veux utiliser une approche streaming intelligente.

Le système doit :

- récupérer les fichiers GH Archive horaires
- les lire en streaming
- parser les événements ligne par ligne
- envoyer les événements directement dans Kafka
- éviter le stockage massif local
- supprimer les fichiers temporaires après traitement

Je veux une architecture :
- pseudo temps réel
- scalable
- moderne
- orientée event streaming

---

# ARCHITECTURE CIBLE SOUHAITÉE

Je veux construire progressivement une architecture proche de :

```txt
GH Archive
    ↓
Python Streaming Producer
    ↓
Kafka
    ↓
Spark Structured Streaming
    ↓
Bronze Layer (Delta)
    ↓
Silver Layer (Delta)
    ↓
Gold Layer (Delta)
    ↓
dbt
    ↓
PostgreSQL / DuckDB
    ↓
Analytics API
    ↓
Realtime Dashboard
````

---

# TECHNOLOGIES À UTILISER

Je veux utiliser :

* Python
* Kafka
* Spark Structured Streaming
* Delta Lake
* Airflow
* dbt
* PostgreSQL
* Docker
* Docker Compose
* GitHub Actions
* Quartz
* Cloudflare Pages

Frontend recommandé :

* Next.js
* Tailwind
* Tremor

---

# IMPORTANT — ARCHITECTURE MEDALLION

Je veux absolument utiliser :

* Bronze
* Silver
* Gold

Je veux que tu expliques :

* le rôle de chaque layer
* quelles données vont dans chaque layer
* les transformations associées
* les optimisations possibles

---

# IMPORTANT — ÉVÉNEMENTS GITHUB À PRIORISER

Je veux principalement utiliser :

* PushEvent
* PullRequestEvent
* WatchEvent
* ForkEvent
* IssuesEvent
* ReleaseEvent

Je veux que tu expliques :

* pourquoi ils sont utiles
* quelles analyses ils permettent
* quelles métriques ils permettent

---

# OBJECTIF DASHBOARD

Je veux construire un dashboard temps réel moderne.

Le dashboard devra montrer :

## Temps réel

* activité GitHub live
* événements par seconde
* feed temps réel

---

## Analytics

* top repositories
* top organisations
* croissance stars/forks
* fréquence des releases
* activité développeurs
* tendances open source

---

## Visualisations

* heatmaps
* timelines
* graphes
* pipelines
* dashboards modernes

---

# IMPORTANT — QUARTZ

Quartz doit rester uniquement :

* documentation technique
* architecture documentation
* setup guides
* portfolio engineering
* captures d’écran
* explications techniques

Le dashboard live ne doit PAS être intégré directement dans Quartz.

---

# IMPORTANT — DÉPLOIEMENT

Je veux utiliser :

* GitHub
* GitHub Actions
* Cloudflare Pages

Je veux une architecture monorepo professionnelle.

Je veux comprendre :

* comment organiser le repository
* comment séparer frontend/dashboard/docs/backend
* comment faire cohabiter Quartz et le dashboard
* comment déployer plusieurs applications depuis le même repo

---

# STRUCTURE REPOSITORY SOUHAITÉE

Je veux une structure proche de :

```txt
repository/
│
├── quartz/
│
├── frontend-dashboard/
│
├── backend/
│
├── kafka/
│
├── spark/
│
├── airflow/
│
├── dbt/
│
├── infrastructure/
│
├── docker/
│
├── scripts/
│
└── docker-compose.yml
```

---

# OBJECTIF PRINCIPAL

Je veux construire :

* un vrai projet portfolio
* un vrai pipeline Data Engineering
* une vraie plateforme analytics moderne

Je veux que le projet démontre :

* architecture distribuée
* streaming
* Data Lakehouse
* analytics engineering
* orchestration
* visualisation
* DevOps/DataOps

---

# CE QUE JE VEUX QUE TU FASSES

Je veux que tu m’accompagnes ÉTAPE PAR ÉTAPE.

Tu ne dois PAS générer directement tout le projet.

Je veux une roadmap progressive.

---

# CE QUE JE VEUX DANS LA RÉPONSE

Je veux :

## 1. Architecture complète du projet

Avec :

* diagrammes
* explications
* composants
* flux de données

---

## 2. Plan de développement étape par étape

Je veux :

* Phase 1
* Phase 2
* Phase 3
* etc.

Avec :

* objectifs
* fichiers à créer
* composants à développer
* validations à effectuer

---

## 3. MVP recommandé

Je veux :

* le plus petit pipeline fonctionnel possible
* les composants minimums
* les priorités techniques

---

## 4. Architecture Kafka

Je veux :

* topics
* schémas événements
* partitionnement
* stratégie ingestion

---

## 5. Architecture Spark

Je veux :

* Spark Structured Streaming
* parsing JSON
* micro-batching
* agrégations
* fenêtres temporelles

---

## 6. Architecture Delta Lake

Je veux :

* Bronze
* Silver
* Gold
* partitionnement
* compaction
* optimisation

---

## 7. Architecture dbt

Je veux :

* modèles analytics
* KPIs
* marts
* métriques business

---

## 8. Airflow

Je veux :

* orchestration
* DAGs
* scheduling
* monitoring

---

## 9. Frontend Dashboard

Je veux :

* architecture frontend
* pages
* composants
* visualisations
* métriques live

---

## 10. Déploiement

Je veux :

* Docker Compose
* GitHub Actions
* Cloudflare Pages
* stratégie CI/CD

---

## 11. Documentation Quartz

Je veux :

* structure docs
* pages importantes
* architecture documentation
* portfolio engineering

---

# IMPORTANT

Je veux une approche :

* réaliste
* professionnelle
* moderne
* progressive
* orientée recrutement Data Engineering

Je veux éviter :

* la complexité inutile
* le sur-engineering prématuré
* les architectures impossibles à maintenir

---

# OBJECTIF FINAL

À la fin :
je veux un projet :

* moderne
* scalable
* professionnel
* impressionnant techniquement
* excellent pour GitHub portfolio
* excellent pour recrutement Data Engineering
* excellent pour démontrer :

  * Kafka
  * Spark
  * Delta Lake
  * dbt
  * streaming
  * analytics engineering
  * DevOps/DataOps

```
```
