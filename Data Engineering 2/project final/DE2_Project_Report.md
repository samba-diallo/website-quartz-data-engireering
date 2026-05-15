# DE2 — Rapport de Projet Final (Track B : GitHub Archive)
**Auteurs** : Samba DIALLO et son binôme.
**Cours** : Data Engineering II (Data-Intensive Workloads) - ESIEE 2025-2026

---

## 1. Cas d'usage et Dataset
**Problème** : Extraire des informations sur l'activité des développeurs open-source, comprendre les rythmes de publications (Push, Pull Requests) et identifier les dépôts les plus influents dans la communauté.
**Dataset** : **GitHub Archive (Track B)**. Le jeu de données fournit une archive horaire (au format `.json.gz`) contenant la quasi-totalité des événements publics de la plateforme GitHub.
**Défis** : Le schéma JSON de GitHub Archive est fortement imbriqué (un champ `payload` polymorphe selon l'`event_type`) et très volumineux. Une mauvaise ingestion provoque rapidement des dépassements de mémoire (`OutOfMemoryError`).

## 2. Système et SLOs (Service Level Objectives)
- **Environnement** : Machine unique locale (Laptop), Spark 4.x (local[*]), Python 3.10.
- **SLOs définis** :
  1. **Latence Pipeline Batch** : Bronze → Gold en moins de 10 min.
  2. **Latence Streaming** : Agrégation fenêtrée en moins de 30 secondes d'intervalle.
  3. **Latence Texte** : Recherche dans l'index inversé en $\le$ 2s par terme.
  4. **Stockage** : Format Parquet occupant $\le$ 60% du volume du CSV brut.
  5. **Qualité LLM** : $\ge$ 80% des textes passent les filtres (longueur, nettoyage).

## 3. Architecture ETL Batch (Medallion)
L'architecture Batch repose sur 3 couches (`outputs/project/`) :
- **Bronze (Landing)** : Les événements JSON sont ingérés tels quels (bruts et immuables) depuis `data/archive/*.json.gz`. 
- **Silver (Cleaned & Typed)** : On aplatit les métadonnées de base (`event_id`, `event_type`, `actor_login`, `repo_name`, `created_at`). **Optimisation mémoire critique** : au lieu d'importer le gigantesque champ struct `payload`, nous n'extrayons *que* les champs nécessaires (le tableau des commits `payload.commits` et les textes de PR) pour alléger l'empreinte de 95% et éviter le *Java heap space OOM*. Les données sont partitionnées par `date`.
- **Gold (Analytics)** : Une table `repo_activity` agrège les événements par jour, par dépôt et par type, prête pour l'exposition BI ou via notre backend DuckDB.

## 4. Ingestion Streaming
Un script simule l'arrivée continue de fichiers horaires dans `data/landing/`.
- **Source** : `FileStreamSource` avec `maxFilesPerTrigger=1`.
- **Fenêtre et Watermark** : Les données sont groupées par `event_type` sur une fenêtre de 5 minutes, avec un **watermark de 10 minutes** basé sur le champ `created_at` (casté en timestamp) pour gérer les données en retard.
- **Sink** : Écriture en mode `append` vers du Parquet, vérifiable via la capture du `query.lastProgress` et l'interface Spark UI.

## 5. Traitement de Texte (Inverted Index)
Nous avons ciblé les messages de commit extraits des `PushEvent`.
- **Preprocessing** : `regexp_replace` (normalisation alpha-numérique), split sur les espaces blancs, et suppression de stop-words courants de l'anglais et du développement logiciel.
- **Index Inversé** : Construit via une agrégation (`collect_list` des `doc_id` et `count`).
- **Gains vs SLOs** : Le stockage en Parquet est nettement plus efficace que le CSV, et le lookup d'un terme spécifique (ex: "fix", "bug") via Spark `filter` respecte le SLO de 2 secondes.

## 6. Charge Itérative : PageRank (Graphe)
Au lieu du clustering, nous avons choisi l'**analyse de graphe** car elle correspond à la topologie naturelle de GitHub (Développeur $\rightarrow$ Dépôt).
- **Graphe construit** : Les arêtes sont les contributions (`PushEvent`, `PullRequestEvent`, `IssuesEvent`) de `actor_login` (source) vers `repo_name` (destination).
- **Algorithme** : PageRank itératif via jointures distribuées. À chaque itération, les nœuds redistribuent leur rang pondéré par un *damping factor* (0.85).
- **Partitionnement** : Le PageRank génère un lourd *shuffle* à chaque jointure. Nous avons mesuré qu'un partitionnement par hachage (`repartition(N, "src")`) réduit les échanges *Exchange* réseau comparé à la distribution par défaut.
- **Convergence** : La différence absolue totale ($\Delta$) entre les rangs successifs diminue à chaque itération, confirmant la convergence.

## 7. Préparation des Données pour LLM
Le but est de préparer un corpus ("LLM Data Readiness") pour du fine-tuning ou un système RAG.
- **Sources textuelles** : Messages de commit et corps/titres de Pull Requests.
- **Filtres de qualité** : Suppression des textes vides, restriction aux messages de longueur $\ge$ 50 caractères (pour filtrer les simples messages *"fix"*), et **déduplication absolue** via le hachage de la chaîne (`xxhash64(text)`).
- Plus de détails sont disponibles dans la **Data Card** (`data_card.md`).

## 8. Design Physique & Optimisations
Des plans `EXPLAIN FORMATTED` ont été générés avant et après nos interventions.
- **Sélection précoce des colonnes** : Dans la couche Silver, réduire le schéma lu et éliminer les structs non nécessaires a sauvé le pipeline d'une erreur OOM.
- **Partition Tuning** : Le format Parquet Silver est partitionné par `date`, permettant au *Predicate Pushdown* d'agir lors du traitement Batch.
- **Coût d'Exchange** : Dans la charge itérative, le coût du `ShuffleExchangeExec` a été contrôlé en s'assurant que les DataFrames partagent la même fonction de partition (hash partitioning).

## 9. Conclusion
Le pipeline complet respecte les contraintes locales et les exigences d'une architecture *Medallion* moderne. Les choix faits face à l'imbrication des JSON de GitHub prouvent que l'analyse du schéma (`printSchema()`) est cruciale. L'intégration de DuckDB (hors notation, pour le backend) permet en aval une exploitation sans latence des couches Gold produites par Apache Spark.
