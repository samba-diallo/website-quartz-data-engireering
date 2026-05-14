# Data Engineering Portfolio - ESIEE Paris

> **Auteur:** DIALLO Samba
> **Professeur:** TAJINI Badr
> **Formation:** Master Data Engineering - ESIEE Paris (2025-2026)
> **Technologies:** Apache Spark, PySpark, Hadoop, Structured Streaming, MLlib, Quartz

**[📖 Accéder au site de documentation Quartz](https://website-quartz-data-engireering.pages.dev/)**

[![Quartz](https://img.shields.io/badge/Built%20with-Quartz-blue)](https://quartz.jzhao.xyz/)
[![Spark](https://img.shields.io/badge/Apache-Spark%204.0-orange)](https://spark.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)

---

## Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Structure du Repository](#structure-du-repository)
- [Data Engineering 1](#data-engineering-1)
- [Data Engineering 2](#data-engineering-2)
- [DevOps & Infrastructure](#devops--infrastructure)
- [Stack Technique](#stack-technique)
- [Installation & Utilisation](#installation--utilisation)
- [Documentation](#documentation)

---

## Vue d'ensemble

Ce repository contient l'ensemble de mes travaux pratiques et projets réalisés dans le cadre des cours **Data Engineering I** et **Data Engineering II** à ESIEE Paris, sous la direction du professeur DIALLO Samba Badr. Il démontre une maîtrise complète des technologies Big Data modernes, du traitement distribué, et des bonnes pratiques d'ingénierie logicielle.

### Points Forts

- **Architecture Monorepo** : Organisation professionnelle avec séparation claire des cours
- **Documentation Complète** : Site web statique généré avec Quartz pour une navigation intuitive
- **Approche Production-Ready** : Métriques, optimisations, preuves d'exécution systématiques
- **CI/CD** : Déploiement automatisé sur Cloudflare Pages
- **Code Quality** : Standards professionnels, commentaires détaillés, notebooks reproductibles

---

## Structure du Repository

```
Data Engineering/
├── Data Engineering 1/          # Fondamentaux Spark & Big Data
│   ├── lab1-practice/          # RDD vs DataFrame
│   ├── lab2-practice/          # Spark SQL & Optimizations
│   ├── lab3-practice/          # Joins & Broadcast
│   └── projet-final/           # Projet intégré DE1
│
├── Data Engineering 2/          # Workloads Intensifs
│   ├── lab0 setup practice/    # Configuration environnement
│   ├── lab1 practice/          # Structured Streaming
│   ├── lab2 practice/          # Indexation & Search
│   ├── lab3 practice/          # Clustering & Iterative
│   └── project final/          # Projet avancé DE2
│
├── content/                     # Sources Quartz (site web)
├── quartz/                      # Configuration Quartz
├── documentation/               # Guides internes
└── Archive_Github.json          # Dataset unifié GitHub Archive
```

---

## Data Engineering 1

### Objectifs Pédagogiques

Maîtrise des fondamentaux du traitement distribué avec Apache Spark :
- Architecture Spark (Driver, Executors, DAG)
- RDD vs DataFrame API
- Spark SQL et optimisations de requêtes
- Stratégies de jointures (Broadcast, Sort-Merge)
- Partitionnement et gestion de la mémoire

### Labs Réalisés

#### Lab 1 : RDD vs DataFrame Performance Analysis

**Objectif :** Comparer les performances entre l'API RDD bas niveau et l'API DataFrame haut niveau.

**Compétences :**
- Manipulation RDD (map, filter, reduceByKey)
- Transformations DataFrame (select, groupBy, agg)
- Analyse de plans d'exécution (explain)
- Métriques de performance (temps, stages, tasks)

**Résultats :**
- DataFrame **3-5x plus rapide** que RDD grâce au Catalyst Optimizer
- Réduction significative du nombre de stages
- Meilleure utilisation de la mémoire avec Tungsten

**Fichiers :**
- `DE1_Lab1_Notebook_EN.ipynb` : Notebook principal
- `proof/plan_rdd.txt` : Plan d'exécution RDD
- `proof/plan_df.txt` : Plan d'exécution DataFrame
- `proof/metrics.png` : Comparaison visuelle

---

#### Lab 2 : Spark SQL & Query Optimization

**Objectif :** Ingestion de données multi-sources et optimisation de requêtes SQL complexes.

**Compétences :**
- Lecture de formats variés (CSV, JSON, Parquet)
- Spark SQL avec jointures multi-tables
- Optimisation de requêtes (predicate pushdown, column pruning)
- Analyse de plans physiques et logiques

**Résultats :**
- Pipeline ETL complet avec 3 sources de données
- Optimisations réduisant le temps d'exécution de **40%**
- Utilisation efficace du cache pour les tables de dimension

**Fichiers :**
- `DE1_Lab2_Notebook_EN.ipynb` : Notebook principal
- `proof/plan_ingest.txt` : Plan d'ingestion
- `proof/plan_fact_join.txt` : Plan de jointure optimisé

---

#### Lab 3 : Advanced Joins & Broadcast Optimization

**Objectif :** Maîtriser les différentes stratégies de jointures et optimiser les performances.

**Compétences :**
- Broadcast Hash Join pour petites tables
- Sort-Merge Join pour grandes tables
- Analyse de skew et repartitionnement
- Optimisation de la mémoire et du shuffle

**Résultats :**
- Broadcast join **10x plus rapide** pour tables < 10MB
- Élimination du shuffle pour jointures dimension-fait
- Stratégies adaptées selon la taille des données

**Fichiers :**
- `DE1_Lab3_Notebook_EN.ipynb` : Notebook principal
- `proof/plan_broadcast.txt` : Plan avec broadcast
- `proof/plan_sortmerge.txt` : Plan sans broadcast

---

#### Projet Final DE1 : Pipeline ETL Complet

**Objectif :** Construire un pipeline ETL production-ready avec optimisations avancées.

**Scope :**
- Ingestion multi-sources (3 datasets)
- Transformations complexes (agrégations, window functions)
- 3 requêtes analytiques optimisées
- Comparaison baseline vs optimized

**Optimisations Appliquées :**
- ✅ Broadcast joins pour tables de dimension
- ✅ Partitionnement stratégique par date
- ✅ Cache des DataFrames réutilisés
- ✅ Predicate pushdown et column pruning
- ✅ Bucketing pour jointures répétées

**Résultats :**
- **Query 1 :** 45% plus rapide (broadcast join)
- **Query 2 :** 60% plus rapide (partitionnement + cache)
- **Query 3 :** 35% plus rapide (bucketing)

**Fichiers :**
- `DE1_Project_Report.md` : Rapport complet
- `proof/baseline_q*.txt` : Plans baseline
- `proof/optimized_q*.txt` : Plans optimisés
- `proof/metrics_*.png` : Graphiques de performance

---

## Data Engineering 2

### Objectifs Pédagogiques

Maîtrise des workloads intensifs en données :
- Structured Streaming en temps réel
- Indexation et recherche distribuée
- Algorithmes itératifs (ML)
- Optimisation de pipelines complexes

### Labs Réalisés

#### Lab 1 : Structured Streaming Pipeline

**Objectif :** Construire un pipeline de streaming temps réel avec agrégations fenêtrées.

**Compétences :**
- Structured Streaming API
- Windowing (tumbling, sliding)
- Watermarks pour late data
- Exactly-once semantics avec checkpoints
- Monitoring avec query.lastProgress

**Architecture :**
```
Source (JSON files) 
  → readStream 
  → Windowed Aggregations (1h windows, 15min watermark)
  → writeStream (Parquet, append mode)
  → Checkpoint (fault tolerance)
```

**Métriques Surveillées :**
- `inputRowsPerSecond` : Débit d'entrée
- `processedRowsPerSecond` : Débit de traitement
- `batchDuration` : Temps par micro-batch
- `totalDelay` : Latence end-to-end

**Optimisations :**
- Partitionnement optimal du sink
- Tuning de la taille des micro-batches
- Gestion efficace des watermarks

**Fichiers :**
- `DE2_Lab1_Notebook_EN.ipynb` : Notebook principal
- `proof/plan_streaming_before.txt` : Plan baseline
- `proof/plan_streaming_after.txt` : Plan optimisé
- `proof/query_progress_*.json` : Métriques streaming

---

#### Lab 2 : Distributed Indexing & Search

**Objectif :** Implémenter un système d'indexation inversée distribuée pour la recherche full-text.

**Compétences :**
- Tokenization et normalisation de texte
- Construction d'index inversé distribué
- Recherche avec scoring TF-IDF
- Optimisation des requêtes de recherche

**Pipeline :**
```
Documents
  → Tokenization (split, lowercase, stopwords)
  → Inverted Index (word → [doc_ids])
  → TF-IDF Scoring
  → Search Query Processing
```

**Résultats :**
- Index de **100K documents** en < 2 minutes
- Recherche en **< 100ms** pour requêtes simples
- Support de requêtes multi-termes avec ranking

**Fichiers :**
- `DE2_Lab2_Notebook_EN.ipynb` : Notebook principal
- `proof/plan_index_build.txt` : Plan de construction d'index
- `proof/plan_query.txt` : Plan de requête

---

#### Lab 3 : Iterative Workloads - Clustering

**Objectif :** Exécuter des algorithmes itératifs (KMeans) avec analyse de convergence et optimisation.

**Compétences :**
- MLlib (KMeans, BisectingKMeans)
- Feature engineering (VectorAssembler, StandardScaler)
- Analyse de convergence et stabilité
- Optimisation du partitionnement pour itérations
- Métriques de clustering (Silhouette score)

**Expériences Menées :**

1. **Sweep k ∈ {4, 6, 8, 10}** : Trouver le nombre optimal de clusters
2. **Stability Analysis** : Tester 5 seeds différentes
3. **Partitioning Experiment** : Impact du nombre de partitions (1, 2, 4, 8, 16)

**Résultats :**
- Meilleur k = **6** (Silhouette = 0.4523)
- Stabilité : σ = 0.0012 (très stable)
- Partitionnement optimal : **4 partitions** (balance shuffle/parallélisme)

**Fichiers :**
- `DE2_Lab3_Notebook_EN.ipynb` : Notebook principal
- `lab3_metrics_log.csv` : Toutes les métriques
- `proof/plan_iterative.txt` : Plan d'exécution
- `proof/summary.txt` : Résumé des résultats

---

#### Projet Final DE2 : [En cours]

**Objectif :** Projet intégré combinant streaming, indexation et ML.

**Status :** En développement

---

## DevOps & Infrastructure

### CI/CD Pipeline

- **GitHub Actions** : Build et tests automatisés
- **Cloudflare Pages** : Déploiement automatique du site Quartz
- **Workflow** : Push → Build → Deploy (< 2 minutes)

### Site Web Documentation

- **Framework** : Quartz (Static Site Generator)
- **URL** : **[https://website-quartz-data-engireering.pages.dev/](https://website-quartz-data-engireering.pages.dev/)**
- **Features** :
  - Navigation intuitive par cours/lab
  - Notebooks rendus en HTML
  - Graphiques et métriques interactifs
  - Recherche full-text
  - Mode sombre/clair

---

## Stack Technique

### Big Data & Processing

- **Apache Spark 4.0.1** : Moteur de traitement distribué
- **PySpark** : API Python pour Spark
- **Hadoop HDFS** : Système de fichiers distribué
- **Parquet** : Format de stockage colonnaire

### Machine Learning

- **Spark MLlib** : Algorithmes ML distribués
- **scikit-learn** : Preprocessing et métriques
- **pandas** : Manipulation de données

### Development & Tools

- **Python 3.10+** : Langage principal
- **Jupyter Notebooks** : Environnement interactif
- **Git** : Versioning
- **VS Code** : IDE

### Documentation & Publishing

- **Quartz** : Static site generator
- **Markdown** : Format de documentation
- **Mermaid** : Diagrammes
- **Cloudflare Pages** : Hébergement

---

## Installation & Utilisation

### Prérequis

```bash
# Java 11 ou 17
java -version

# Python 3.10+
python --version

# Spark 4.0.1
spark-submit --version
```

### Cloner le Projet

```bash
# Cloner le repository
git clone https://github.com/[votre-username]/data-engineering-portfolio.git

# Accéder au répertoire
cd data-engineering-portfolio
```

### Installation des Dépendances

```bash
# Installer les dépendances Python
pip install -r requirements.txt

# Configurer Spark (optionnel)
export SPARK_HOME=/path/to/spark
export PATH=$SPARK_HOME/bin:$PATH
```

### Exécution des Notebooks

```bash
# Lancer Jupyter
jupyter notebook

# Ou utiliser VS Code avec l'extension Jupyter
code .
```

### Build du Site Web

```bash
# Installer Quartz
npm install

# Build local
npx quartz build --serve

# Accéder au site
open http://localhost:8080
```

---

## Documentation

### Guides Internes

- **[MISE_A_JOUR_SITE.md](documentation/MISE_A_JOUR_SITE.md)** : Guide de mise à jour du site
- **[PLAN.md](PLAN.md)** : Architecture et plan de réorganisation
- **[ARCHITECTURE.md](documentation/ARCHITECTURE.md)** : Architecture détaillée

### Conventions

- **Nommage** : `labX practice/` pour les labs, `project final/` pour les projets
- **Notebooks** : Format `.ipynb` avec cellules markdown explicatives
- **Preuves** : Dossier `proof/` dans chaque lab (plans, métriques, screenshots)
- **Commits** : Format conventionnel (`feat:`, `fix:`, `docs:`, etc.)

---

## Métriques du Projet

| Métrique | Valeur |
|----------|--------|
| **Labs Complétés** | 7/7 (DE1: 3 + Projet, DE2: 3) |
| **Notebooks** | 10+ |
| **Lignes de Code** | ~5000+ |
| **Optimisations** | 15+ techniques appliquées |
| **Gain de Performance** | 30-60% selon les cas |
| **Documentation** | 100% des labs documentés |

---

## Compétences Démontrées

### Techniques

- Architecture Spark (Driver, Executors, DAG)
- RDD & DataFrame API
- Spark SQL & Catalyst Optimizer
- Structured Streaming
- MLlib (Clustering, Feature Engineering)
- Optimisation de requêtes
- Partitionnement et shuffle management
- Broadcast joins
- Caching strategies
- Watermarks & late data handling

### Soft Skills

- Documentation technique professionnelle
- Analyse de performance et métriques
- Résolution de problèmes complexes
- Approche méthodique et reproductible
- Communication claire des résultats

---


## Licence

Ce projet est réalisé dans un cadre académique à ESIEE Paris sous la direction du professeur TAJINI Badr.
© 2025-2026 DIALLO Samba @ DIOP Mouhamed- Tous droits réservés.

---

## Remerciements

- **ESIEE Paris** : Formation Data Engineering
- **Professeur  Badr TAJINI** : Encadrement et enseignement
- **Apache Spark Community** : Documentation et support
- **Quartz** : Framework de documentation
- **Cloudflare** : Hébergement gratuit

---

<div align="center">


Made by DIALLO Samba @ DIOP Mouhamed

</div>