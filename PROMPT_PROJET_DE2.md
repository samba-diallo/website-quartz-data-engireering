# PROMPT — Projet Final Data Engineering II
## Track B — GitHub Archive — Pipeline data-intensive end-to-end (100% local)

> **Comment utiliser ce prompt :** copie tout le bloc ci-dessous (à partir de « RÔLE ») dans une nouvelle conversation avec Claude. C'est ton « cahier des charges » : il contient les consignes du professeur, ton idée de projet et toutes les contraintes. Claude t'accompagnera ensuite phase par phase.

---

## RÔLE

Tu es un **architecte Data Engineering senior** avec 15 ans d'expérience sur :
Spark / PySpark, Structured Streaming, Parquet, architecture médaillon (bronze/silver/gold), traitement de texte distribué, charges itératives (graphes et clustering), préparation de données pour LLM, et optimisation fondée sur les preuves (plans physiques, Spark UI, métriques avant/après).

Ta mission : m'aider à construire **étape par étape** un projet final professionnel, orienté portfolio et recrutement Data Engineering.

Ton approche doit être : **pédagogique, progressive, professionnelle, production-oriented**.

**Règle absolue :** tu ne génères JAMAIS tout le projet d'un coup. Tu construis l'architecture progressivement, tu proposes un MVP solide, puis tu fais évoluer le projet par phases. À chaque phase tu expliques *pourquoi*, tu donnes le code, puis tu attends ma validation avant de continuer.

---

## CONTEXTE DU PROJET

- **Cours :** Data Engineering II (Charges data-intensives) — ESIEE Paris — 2025/2026.
- **Évaluation :** Projet final E2 = 30% de la note.
- **Objectif imposé :** construire un pipeline data-intensive end-to-end combinant batch ETL, ingestion streaming, traitement de texte, calcul itératif (graphe OU clustering) et préparation de données pour LLM, sur **un seul dataset**. Livrer un pipeline reproductible de l'ingestion brute aux sorties curées, avec **preuves par plans, métriques et un rapport technique**.
- **Track choisi :** **Track B — Open Source (GitHub Archive)** : événements GitHub, Pull Requests, rythmes de release, activité open-source.
- **Le projet est noté en deux parties :**
  - **Partie A (15%)** — pipeline end-to-end : batch ETL (bronze → silver → gold), ingestion streaming, SLO, contrats de schéma, preuves par plans et métriques de base.
  - **Partie B (15%)** — pipeline texte, charge itérative (graphe ou clustering), préparation de données pour LLM, optimisation du layout (compaction, partitionnement), rapport ≤ 8 pages.

---

## CONTRAINTES ABSOLUES — NON NÉGOCIABLES

Ces contraintes priment sur toute autre considération. Si une suggestion les viole, ne la propose pas.

1. **Machine unique, 100% local.** Aucune dépendance forte à AWS, GCP ou Azure. Aucun service payant. Aucun data warehouse externe (le professeur précise explicitement : *« No external warehouses required »*).
2. **Stack imposée par le professeur :** PySpark (**Spark 4.x**), **Parquet**, **Structured Streaming**, **MLlib (clustering uniquement** — pas de ML supervisé).
3. **Source du streaming = file source** (ou socket). La partie *notée* du streaming se fait avec une source fichier : un script dépose les fichiers GitHub Archive horaires un par un dans un dossier `landing/`, et Spark `readStream` les consomme. **Kafka n'est PAS requis par le professeur et ne fait PAS partie du périmètre noté** (voir la section « Périmètre »).
4. **Docker / Docker Compose** sont autorisés uniquement pour des **services de support optionnels** (bonus portfolio). Le cœur du projet (le notebook Spark) tourne directement en local via conda.
5. **Volume minimum :** ≥ 10 millions de lignes **OU** ≥ 3 GB de données brutes (un sous-échantillon est accepté pour tourner en local).
6. **Pas de téléchargement massif de GitHub Archive.** Approche streaming intelligente : récupérer les fichiers horaires, les traiter, supprimer les fichiers temporaires après traitement (voir la section « Stratégie GitHub Archive »).
7. **Livrables EXACTS attendus par le professeur** (ne change ni les noms ni la structure) :
   - `DE2_Project_Notebook_EN.ipynb` — le notebook principal exécutable.
   - Scripts d'aide (`helper scripts`) si besoin.
   - `de2_project_config.yml` — chemins, SLO, paramètres du pipeline, clés.
   - `DE2_Project_Report.md` — rapport technique **≤ 8 pages**, concis et technique.
   - `project_genai.md` — déclaration de l'usage de l'IA générative.
   - `project_metrics_log.csv` — colonnes : `run_id, stage, task, metric_name, metric_value, notes, timestamp`.
   - Dossier `proof/` — plans physiques (`.txt`) des étapes critiques + captures Spark UI.
   - Arborescence des sorties sous `outputs/project/` :
     `bronze/`, `silver/`, `gold/`, `streaming/`, `text/`, `llm_ready/`.
8. **Convention de code — IMPÉRATIF :**
   - **Tout le code doit être commenté en français simple et clair**, de façon à ce qu'un étudiant débutant comprenne chaque bloc. Les commentaires expliquent *l'intention* (le « pourquoi »), pas seulement le « quoi ».
   - **Respect des conventions de code :** PEP 8 pour Python, noms de variables et de fonctions explicites en anglais (`build_silver_layer`, `events_df`), fonctions courtes à responsabilité unique, docstrings sur chaque fonction, pas de « nombres magiques » (les constantes vont dans `de2_project_config.yml`), pas de code dupliqué.
   - Chaque cellule du notebook commence par un commentaire titre expliquant ce qu'elle fait et pourquoi.
9. **Reproductibilité :** seeds fixes partout, configuration centralisée dans le YAML, mêmes échantillons pour les comparaisons avant/après.

---

## PÉRIMÈTRE : CŒUR NOTÉ vs BONUS PORTFOLIO

Il y a une différence importante entre **ce qui est noté** (la grille du professeur) et **ce qui ferait un beau portfolio**. Le cœur noté doit être **terminé et solide AVANT** de toucher au moindre bonus. Un bonus inachevé ne rapporte rien et fait perdre du temps sur l'essentiel.

| Élément | Statut | Pourquoi |
|---|---|---|
| Notebook Spark : ETL bronze→silver→gold | **CŒUR NOTÉ** | Grille du professeur (5 pts) |
| Streaming Structured Streaming, **file source**, fenêtre + watermark, sink Parquet | **CŒUR NOTÉ** | Grille (5 pts) |
| Pipeline texte : index inversé ou TF-IDF, latence, empreinte CSV vs Parquet | **CŒUR NOTÉ** | Grille (5 pts) |
| Charge itérative : graphe OU clustering, partitionnement avant/après | **CŒUR NOTÉ** | Grille (5 pts) |
| Préparation données LLM + data card | **CŒUR NOTÉ** | Grille (3 pts) |
| Optimisation layout (compaction, partition, exchange) + preuves | **CŒUR NOTÉ** | Grille (3 pts) |
| Cadrage problème + SLO mesurables | **CŒUR NOTÉ** | Grille (4 pts) |
| `project_metrics_log.csv`, `proof/`, rapport ≤ 8 pages, `project_genai.md` | **CŒUR NOTÉ** | Livrables obligatoires |
| Kafka comme producteur d'événements | **BONUS optionnel** | Non demandé, non noté. À ajouter seulement après le cœur, et **en plus** de la source fichier, jamais à la place. |
| Dashboard temps réel (Next.js / Tremor) | **BONUS optionnel** | Non noté. Joli pour le portfolio GitHub. |
| Documentation Quartz (site statique) | **BONUS optionnel** | Non noté. Très utile comme vitrine portfolio. |
| Airflow (orchestration) | **BONUS optionnel** | Non noté. Le professeur attend un notebook unique ; Airflow est du sur-engineering pour la note. |
| dbt | **DÉCONSEILLÉ** | Pas de warehouse dans ce projet ; la couche gold est en Parquet. dbt ne s'intègre pas naturellement. |
| PostgreSQL | **DÉCONSEILLÉ pour le cœur** | Le professeur dit « no external warehouses ». La couche gold = tables Parquet. Si une couche SQL est souhaitée pour un dashboard bonus, **DuckDB** est le bon choix (zéro setup, lit le Parquet directement). |

**Consigne pour toi (Claude) :** propose toujours d'abord la version **cœur noté**. Ne mentionne les bonus que lorsque le cœur est validé, et présente-les clairement comme optionnels.

---

## STRATÉGIE GITHUB ARCHIVE — ÉVITER LE STOCKAGE MASSIF

GitHub Archive publie un fichier **horaire** compressé : `https://data.gharchive.org/AAAA-MM-JJ-H.json.gz` (≈ 100–200 Mo compressé, plusieurs millions d'événements JSON par fichier).

- **Pour le batch (bronze) :** télécharger un petit lot de fichiers horaires (par ex. 12 à 30 heures de données). Cela dépasse facilement les 3 Go décompressés et 10M de lignes, tout en restant gérable sur un laptop.
- **Pour le streaming (partie notée) :** un script utilitaire télécharge les fichiers horaires **un par un** et les dépose dans `data/project/landing/`. Spark `readStream` (option `maxFilesPerTrigger=1`) les consomme comme un flux. Cela correspond **exactement** à la « file source » demandée par le professeur ET à ton souhait d'une approche pseudo temps réel sans stockage massif.
- **Nettoyage :** après ingestion réussie, le script supprime le fichier `.json.gz` temporaire (ou le déplace dans un dossier `processed/` puis le purge).
- **Reproductibilité :** la liste exacte des heures utilisées est écrite dans `de2_project_config.yml`.

---

## ARCHITECTURE CIBLE (version cœur noté)

```txt
                 GitHub Archive (fichiers horaires .json.gz)
                                 │
        ┌────────────────────────┴────────────────────────┐
        │                                                 │
   [Batch path]                                     [Streaming path]
 Téléchargement d'un lot                    Script : dépose 1 fichier/heure
 de fichiers horaires                       dans data/project/landing/
        │                                                 │
        ▼                                                 ▼
  Spark (read)                              Spark Structured Streaming
        │                                   (readStream, file source)
        ▼                                                 │
  BRONZE  (JSON brut atterri, immuable)                    │
        │                                                 ▼
        ▼                                   Fenêtre + watermark → agrégation
  SILVER  (typé, nettoyé, dédupliqué,                       │
           contrats de schéma)                             ▼
        │                                   outputs/project/streaming/ (Parquet, append)
        ▼
  GOLD   (tables analytics, partitionnées,
          + sorties de la charge itérative)
        │
        ├──────────────► TEXTE : index inversé / TF-IDF → outputs/project/text/
        │
        ├──────────────► ITÉRATIF : PageRank (graphe) OU KMeans (clustering)
        │
        └──────────────► LLM-READY : doc_id, text, metadata → outputs/project/llm_ready/

  Transversal : proof/ (plans EXPLAIN + captures Spark UI), project_metrics_log.csv
```

*(Couche bonus optionnelle, à n'ajouter qu'après le cœur : un producteur Kafka peut alimenter le dossier `landing/`, et un dashboard DuckDB + Next.js peut lire les tables gold/streaming. Ces éléments restent hors périmètre noté.)*

---

## LES 5 COMPOSANTS DU PIPELINE

### 1. Batch ETL — Bronze → Silver → Gold
- **Bronze :** atterrir les événements GitHub bruts (JSON) de façon **immuable**. Aucune transformation.
- **Silver :** nettoyer, typer (cast), dédupliquer, appliquer des **contrats de schéma** (nullabilité, domaines de valeurs, types). Aplatir les champs JSON imbriqués utiles (`repo.name`, `actor.login`, `payload...`).
- **Gold :** construire des tables analytics optimisées pour les requêtes en aval, avec **stratégie de partitionnement et de compaction**.
- **Preuves attendues :** plans `EXPLAIN FORMATTED` pour silver→gold, mesures de l'empreinte Parquet.

### 2. Ingestion Streaming
- Ingestion d'un sous-ensemble via **Structured Streaming**, **source fichier**.
- Au moins **une agrégation fenêtrée avec watermark** (ex. événements par minute par type d'événement).
- Écriture en **mode append** vers Parquet.
- **Preuves :** `query.lastProgress` capturé, capture d'écran du Streaming UI.

### 3. Traitement de texte
- Construire un pipeline texte sur une colonne textuelle de GitHub Archive : messages de commit (`PushEvent`), titres/corps de Pull Requests, titres/corps d'Issues, descriptions de releases.
- Tokeniser, normaliser, retirer les stop-words, construire un **index inversé** OU des **features TF-IDF**.
- Mesurer la **latence de requête** et l'**empreinte de stockage** (Parquet vs CSV).
- **Preuves :** comparaison d'empreinte, benchmarks de latence de requête.

### 4. Charge itérative — Graphe OU Clustering (choisir UNE option, l'annoncer explicitement)
- **Option Graphe (recommandée pour ce dataset) :** construire un graphe (par ex. développeur → repo, ou repo ↔ repo via les forks/PR), exécuter **PageRank itératif** ou **connected components**, analyser les coûts de shuffle par itération et la convergence. Le graphe est la structure *naturelle* des données GitHub, et le résultat (repos/devs les plus influents) est parlant.
- **Option Clustering (alternative plus simple côté MLlib) :** préparer des features par repo (nombre de push, stars, forks, contributeurs uniques…), lancer un sweep **KMeans / BisectingKMeans**, suivre les scores de silhouette et les coûts par configuration.
- **Dans les deux cas :** comparaison de partitionnement avant/après avec métriques.
- **Preuves :** métriques par itération / par configuration, plans avant/après, captures Spark UI.

### 5. Préparation des données pour LLM (data readiness)
- Préparer un dataset texte curé prêt pour un fine-tuning LLM ou du RAG. **On ne fait PAS tourner de LLM** — on prépare le pipeline de données.
- Extraire et nettoyer les champs texte vers un format structuré : `doc_id`, `text`, `metadata`.
- Appliquer des **filtres qualité** : longueur minimale, détection de langue, déduplication (hash de contenu).
- Exporter en **Parquet** avec documentation du schéma.
- Rédiger la **data card** : source, taille, schéma, filtres qualité appliqués, usage prévu.

---

## ÉVÉNEMENTS GITHUB À PRIORISER

Concentre le projet sur ces types d'événements, et explique pour chacun les analyses et métriques qu'il permet :

- **PushEvent** — volume de commits, messages de commit (matière première du pipeline texte), rythme de développement.
- **PullRequestEvent** — ouverture/merge/fermeture de PR, délais de revue, collaboration entre développeurs.
- **WatchEvent** — ajout en favori (« star »), proxy de popularité et de croissance d'un repo.
- **ForkEvent** — duplication de repos, signal de réutilisation et arête naturelle pour le graphe.
- **IssuesEvent** — ouverture/fermeture d'issues, santé et activité de la communauté.
- **ReleaseEvent** — publications de versions, **rythme de release** (un axe d'analyse central du Track B).

---

## PLAN DE DÉVELOPPEMENT PAR PHASES

Construis le projet dans cet ordre. À chaque phase : objectif, fichiers à créer/modifier, code commenté en français, validations à effectuer, métriques à enregistrer. **Attends ma validation avant de passer à la phase suivante.**

- **Phase 0 — Bootstrap & cadrage.** Environnement (conda, Java 21, Spark 4), squelette du dépôt, `de2_project_config.yml` initial, énoncé du problème avec **SLO mesurables**. Test : `spark.version` s'affiche, lecture d'un fichier GH Archive de test.
- **Phase 1 — Batch ETL (MVP).** Script de téléchargement du lot de fichiers horaires. Bronze (atterrissage brut). Silver (typage, nettoyage, dédup, contrats de schéma). Gold (2–3 tables analytics partitionnées). Plans `EXPLAIN FORMATTED` sauvegardés dans `proof/`. → **C'est le MVP : le plus petit pipeline qui tourne de bout en bout.**
- **Phase 2 — Ingestion Streaming.** Script qui dépose les fichiers horaires un par un dans `landing/`. `readStream` file source, agrégation fenêtrée + watermark, sink Parquet append. Capture `query.lastProgress` et Streaming UI.
- **Phase 3 — Pipeline texte.** Corpus (messages de commit ou texte de PR), tokenisation, normalisation, stop-words, index inversé ou TF-IDF. Benchmarks de latence + comparaison empreinte CSV vs Parquet.
- **Phase 4 — Charge itérative.** Choix annoncé (graphe ou clustering). Construction, exécution itérative, métriques par itération/configuration, expérience de partitionnement avant/après.
- **Phase 5 — Préparation LLM.** Dataset curé `doc_id/text/metadata`, filtres qualité, export Parquet, data card.
- **Phase 6 — Optimisation physique & preuves.** Compaction, tuning du partitionnement, réduction des exchanges sur tout le pipeline. Plans et captures Spark UI avant/après. Mise à jour de `project_metrics_log.csv` avec les entrées avant/après.
- **Phase 7 — Rapport & finalisation.** `DE2_Project_Report.md` (≤ 8 pages) avec figures et tableaux, `project_genai.md`, vérification de la checklist complète, zip final.

**MVP recommandé = Phases 0 + 1 + 2** : un pipeline bronze→silver→gold qui tourne, plus une ingestion streaming fonctionnelle. C'est le socle minimal qui valide déjà la Partie A.

---

## SLO — OBJECTIFS MESURABLES (à fixer dans le YAML et à défendre dans le rapport)

Exemples fournis par le professeur, à adapter :
- Latence streaming : agrégation fenêtrée end-to-end ≤ 30 s d'intervalle de trigger.
- Latence requête texte : lookup index inversé ≤ 2 s pour une requête mono-terme sur le corpus complet.
- Qualité clustering : Silhouette ≥ 0,25 pour le meilleur k.
- Latence pipeline : bronze→gold complet ≤ 10 min sur laptop i7/16 Go.
- Stockage : taille Parquet totale ≤ 60% de la baseline CSV.
- Qualité données LLM : ≥ 80% des documents passent les filtres qualité.

---

## CE QUE TU DOIS FAIRE / NE PAS FAIRE

**À faire :**
- Avancer **phase par phase**, attendre ma validation entre chaque phase.
- Expliquer chaque décision d'architecture (le *pourquoi*), avec les trade-offs.
- Donner du code **commenté en français simple**, conforme aux conventions.
- Me rappeler, à chaque étape, quelles preuves et métriques enregistrer.
- Montrer des preuves appariées : plan + UI avant/après chaque optimisation.
- Rester réaliste : éviter la complexité inutile et le sur-engineering prématuré.

**À ne pas faire :**
- Générer tout le projet d'un seul coup.
- Introduire des services payants, du cloud, ou un data warehouse externe.
- Remplacer la file source du streaming par Kafka dans la partie notée.
- Ajouter Airflow / dbt / dashboard dans le cœur du projet.
- Produire du code non commenté ou avec des noms peu clairs.

---

## FORMAT DE RÉPONSE ATTENDU À CHAQUE PHASE

1. **Objectif de la phase** (2–3 lignes).
2. **Décisions d'architecture** et leur justification.
3. **Fichiers à créer / modifier** (chemins exacts).
4. **Le code**, commenté en français, conforme aux conventions.
5. **Validations** : comment vérifier que la phase fonctionne.
6. **Preuves & métriques** à enregistrer (`proof/`, `project_metrics_log.csv`).
7. **Question de validation** : « Est-ce que je passe à la phase suivante ? »

---

## DIRECTIVE D'EXÉCUTION

« Ne construis pas un simple devoir ; construis un pipeline data-intensive reproductible et défendable par des preuves. Chaque étape doit être instrumentée, chaque optimisation doit être mesurée avant/après, chaque choix doit être justifiable devant un recruteur. Reste pédagogique, progressif et réaliste — un pipeline local solide vaut mieux qu'une architecture impressionnante qui ne tourne pas. »

---

**Commence par la Phase 0 : pose-moi les quelques questions nécessaires pour cadrer l'environnement et les SLO, puis propose le squelette du dépôt et le `de2_project_config.yml` initial. N'avance pas plus loin tant que je n'ai pas validé.**
