# GUIDE DES TECHNOLOGIES — Projet Data Engineering II
## Comment utiliser chaque outil, faut-il un compte, et lesquels garder

> Ce guide accompagne le fichier `PROMPT_PROJET_DE2.md`. Il classe chaque technologie en **CŒUR** (imposé / noté), **BONUS** (portfolio, optionnel) ou **DÉCONSEILLÉ**, explique comment l'utiliser en local, et indique si un compte est nécessaire.

---

## Tableau de synthèse

| Technologie | Statut | Compte requis ? | Coût |
|---|---|---|---|
| Python + conda | CŒUR | Non | Gratuit |
| Java (OpenJDK 21) | CŒUR | Non | Gratuit |
| Spark 4.x / PySpark | CŒUR | Non | Gratuit |
| Parquet | CŒUR | Non | Gratuit (format de fichier) |
| Structured Streaming | CŒUR | Non | Gratuit (inclus dans Spark) |
| MLlib | CŒUR | Non | Gratuit (inclus dans Spark) |
| GitHub Archive (dataset) | CŒUR | Non | Gratuit |
| JupyterLab | CŒUR | Non | Gratuit |
| Git + GitHub | CŒUR (rendu) | **Oui** (gratuit) | Gratuit |
| GraphFrames | CŒUR si option graphe | Non | Gratuit |
| DuckDB | BONUS recommandé | Non | Gratuit |
| Docker / Docker Compose | BONUS | Non (compte Docker Hub optionnel) | Gratuit |
| Kafka | BONUS | Non | Gratuit (en local via Docker) |
| Quartz | BONUS (documentation) | Non | Gratuit |
| GitHub Actions | BONUS | Oui (compte GitHub) | Gratuit (quota généreux) |
| Cloudflare Pages | BONUS | **Oui** (gratuit) | Gratuit (offre gratuite) |
| Next.js / Tailwind / Tremor | BONUS (dashboard) | Non | Gratuit |
| Airflow | BONUS (déconseillé pour la note) | Non | Gratuit |
| PostgreSQL | DÉCONSEILLÉ pour le cœur | Non | Gratuit |
| dbt | DÉCONSEILLÉ ici | Non | Gratuit |

---

# 1. Le CŒUR — ce qui est imposé et noté

## Python + conda
**Rôle :** langage du projet et gestionnaire d'environnement isolé.
**Compte ?** Non.
**Installation :** installer Miniconda, puis créer un environnement dédié :
```bash
conda create -n de2 python=3.10
conda activate de2
```
**Bon à savoir :** un environnement conda par projet évite les conflits de versions. Toutes les dépendances Python du projet s'installent dedans.

## Java (OpenJDK 21)
**Rôle :** Spark tourne sur la JVM. Spark 4 a besoin de Java 17 ou 21.
**Compte ?** Non.
**Installation :** via conda (`conda install -c conda-forge openjdk=21`) ou le gestionnaire de paquets du système. Vérifier avec `java -version`.
**Bon à savoir :** si Spark ne démarre pas, c'est presque toujours un problème de `JAVA_HOME` ou de version de Java.

## Spark 4.x / PySpark
**Rôle :** le moteur de calcul distribué — c'est le centre du projet (ETL, streaming, texte, itératif, LLM prep).
**Compte ?** Non. Logiciel libre.
**Installation :** le plus simple est `pip install pyspark` dans l'environnement conda. Alternative : télécharger Spark 4.0.0 précompilé depuis le site Apache.
**Comment ça tourne en local :** Spark s'exécute en mode `local[*]` — il utilise tous les cœurs de ta machine, sans cluster. C'est suffisant pour ce projet.
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("de2-project").master("local[*]").getOrCreate()
```
**Spark UI :** une interface web (par défaut `http://localhost:4040`) montre les jobs, les stages, le shuffle, le spill. Tu y prendras les **captures d'écran** demandées comme preuves.

## Parquet
**Rôle :** format de fichier colonnaire, compressé. C'est le format de sortie de silver, gold, streaming, text et llm_ready.
**Compte ?** Non. Ce n'est pas un service, juste un format.
**Comment l'utiliser :** rien à installer, c'est intégré à Spark : `df.write.parquet(...)` et `spark.read.parquet(...)`.
**Pourquoi :** beaucoup plus compact et rapide à requêter que le CSV — le projet demande justement de **mesurer** ce gain.

## Structured Streaming
**Rôle :** le module de streaming de Spark. Pour ce projet : **source fichier**, agrégation fenêtrée avec watermark, sink Parquet en mode append.
**Compte ?** Non. C'est inclus dans Spark.
**Comment ça marche ici :** un script dépose les fichiers GitHub Archive horaires un par un dans un dossier `landing/`. Spark `readStream` les détecte et les traite comme un flux (`maxFilesPerTrigger=1`). C'est la « file source » demandée par le professeur — pas besoin de Kafka.

## MLlib
**Rôle :** la bibliothèque de machine learning de Spark. Pour ce projet, **clustering uniquement** : `KMeans`, `BisectingKMeans`, `ClusteringEvaluator`, `VectorAssembler`, `StandardScaler`.
**Compte ?** Non. Inclus dans Spark.
**Quand l'utiliser :** seulement si tu choisis l'option **clustering** pour la charge itérative. Si tu choisis l'option **graphe**, tu ne l'utilises pas.

## JupyterLab
**Rôle :** l'environnement de notebook. Le livrable principal est `DE2_Project_Notebook_EN.ipynb`.
**Compte ?** Non.
**Installation :** `pip install jupyterlab` dans l'environnement conda, puis `jupyter lab`.

## Git + GitHub
**Rôle :** versionnage du code et **dépôt de rendu** (le projet se rend sur GitHub).
**Compte ?** **Oui — un compte GitHub gratuit est nécessaire** (tu en as probablement déjà un).
**Installation :** installer `git` localement. Créer un dépôt sur github.com.
**Bon à savoir :** commite régulièrement, avec des messages clairs. Ajoute un `.gitignore` pour ne PAS versionner les gros fichiers de données (`data/`, `outputs/`) ni les fichiers temporaires.

## GraphFrames
**Rôle :** bibliothèque pour les algorithmes de graphe sur Spark (PageRank, connected components).
**Compte ?** Non.
**Quand l'utiliser :** seulement si tu choisis l'option **graphe** pour la charge itérative. Alternative sans GraphFrames : implémenter PageRank avec des **joins itératifs manuels** en Spark SQL (le professeur l'autorise explicitement).
**Installation :** se charge comme package Spark au démarrage de la session.

---

# 2. Les BONUS — bien pour le portfolio, mais après le cœur

> Ces outils ne sont **pas notés**. Ils rendent le projet plus impressionnant sur ton GitHub, mais ne les aborde **qu'une fois le cœur terminé et solide**. Un bonus inachevé fait perdre des points sur l'essentiel.

## DuckDB — *le bonus recommandé*
**Rôle :** base de données analytique embarquée (comme « SQLite pour l'analytique »). Elle **lit directement les fichiers Parquet** sans import.
**Compte ?** Non.
**Installation :** `pip install duckdb`. C'est tout — aucun serveur à lancer.
**Pourquoi c'est le bon choix ici :** si tu veux une couche SQL pour explorer tes tables gold ou alimenter un dashboard, DuckDB le fait avec zéro configuration : `SELECT * FROM 'outputs/project/gold/*.parquet'`. C'est l'alternative locale et gratuite à PostgreSQL pour ce projet (voir la section verdict plus bas).

## Docker / Docker Compose
**Rôle :** lancer des services de support (Kafka, etc.) de façon isolée et reproductible.
**Compte ?** Non pour l'usage de base. Un compte Docker Hub (gratuit) sert seulement si tu publies tes propres images.
**Installation :** Docker Desktop (Windows/Mac) ou Docker Engine + plugin Compose (Linux).
**Comment ça marche :** un fichier `docker-compose.yml` décrit les services ; `docker compose up` les démarre tous. Utile uniquement pour la couche bonus — le cœur du projet (le notebook Spark) tourne directement en conda, sans Docker.

## Kafka
**Rôle :** plateforme de streaming d'événements (un « tube » entre producteurs et consommateurs).
**Compte ?** Non — en local via Docker Compose, tout est gratuit et sans inscription.
**Installation :** un service `kafka` dans le `docker-compose.yml` (les images Bitnami ou Confluent sont les plus simples).
**Honnêteté importante :** **le professeur ne demande PAS Kafka.** Sa consigne dit « file source or socket » pour le streaming, et son notebook modèle utilise une source fichier. Kafka est donc un **bonus pur**. Si tu y tiens pour le portfolio : garde la source fichier pour la partie notée, et ajoute Kafka **en plus**, par exemple comme producteur qui alimente le dossier `landing/`, ou comme démo séparée. Ne remplace jamais la file source notée par Kafka.

## Quartz
**Rôle :** générateur de site statique pour transformer des notes Markdown en site de documentation (c'est d'ailleurs ce que ton professeur utilise pour publier les consignes).
**Compte ?** Non — c'est un outil local. Le déploiement se fait via GitHub Pages ou Cloudflare Pages.
**Usage dans le projet :** Quartz doit rester **uniquement de la documentation** : architecture, guides de setup, captures d'écran, explications techniques, vitrine portfolio. **Le dashboard live ne doit PAS être intégré dans Quartz.**
**Installation :** cloner le dépôt Quartz, déposer tes fichiers Markdown dans `content/`, `npx quartz build`.

## GitHub Actions
**Rôle :** CI/CD — exécuter automatiquement des tâches à chaque push (tests, build de la doc, déploiement).
**Compte ?** Oui — inclus avec ton compte GitHub. L'offre gratuite suffit largement pour un projet étudiant.
**Usage dans le projet :** un workflow simple, par exemple : vérifier que le notebook s'exécute sans erreur, ou builder et déployer le site Quartz.
**Installation :** rien à installer — il suffit d'ajouter un fichier `.github/workflows/*.yml` dans le dépôt.

## Cloudflare Pages
**Rôle :** hébergement gratuit de sites statiques (pour publier la doc Quartz et/ou le dashboard).
**Compte ?** **Oui — un compte Cloudflare gratuit est nécessaire.** L'offre gratuite est généreuse et sans carte bancaire.
**Usage :** connecter le dépôt GitHub, Cloudflare build et déploie automatiquement à chaque push.
**Alternative :** GitHub Pages fait la même chose et ne demande aucun compte supplémentaire — c'est même plus simple si tu veux éviter une inscription de plus.

## Next.js / Tailwind / Tremor
**Rôle :** stack pour construire le dashboard temps réel (Next.js = framework React, Tailwind = CSS, Tremor = composants de graphiques/dashboards).
**Compte ?** Non.
**Installation :** `npx create-next-app`, puis ajout de Tailwind et Tremor via npm.
**Honnêteté importante :** le dashboard n'est **pas noté**. C'est un beau plus pour le portfolio GitHub, mais il vient en toute fin de projet, après que les 5 composants du pipeline sont terminés et que le rapport est écrit.

## Airflow
**Rôle :** orchestrateur de workflows (planifier et enchaîner des tâches via des DAGs).
**Compte ?** Non — en local via Docker.
**Honnêteté importante :** le professeur attend **un notebook unique** exécutable. Airflow est de l'**orchestration de production** — utile dans la vraie vie, mais c'est du **sur-engineering pour ce projet** et ce n'est pas noté. Si tu veux montrer que tu connais l'orchestration, un seul petit DAG de démonstration en bonus suffit ; n'en fais pas le cœur de l'architecture.

---

# 3. Les DÉCONSEILLÉS pour ce projet

## dbt
**Ce que c'est :** outil de transformation analytique qui s'exécute **par-dessus un data warehouse** (modèles SQL, tests, documentation).
**Pourquoi c'est déconseillé ici :** dbt suppose un warehouse SQL comme destination. Or le professeur dit explicitement « no external warehouses required », et ta couche gold est constituée de **tables Parquet** produites par Spark. dbt ne s'intègre pas naturellement dans ce schéma. Il existe `dbt-duckdb` qui ferait techniquement le pont, mais cela ajoute une couche pour zéro point de notation et complexifie le pipeline. **Recommandation : ne pas utiliser dbt sur ce projet.** Les transformations analytiques se font directement en PySpark (couche gold), c'est ce qui est attendu et noté.

---

# 4. VERDICT — PostgreSQL est-il une bonne idée pour ce projet ?

**Réponse courte : non, pas pour le cœur du projet. Utilise Parquet (imposé) et, si tu veux une couche SQL pour un dashboard bonus, utilise DuckDB.**

**Pourquoi :**

- **Le professeur l'exclut implicitement.** La consigne dit « no external warehouses required » et « Platform: single machine. PySpark, Parquet, Structured Streaming ». La couche gold attendue, ce sont des **tables analytics en Parquet**, pas une base relationnelle.
- **La grille de notation ne récompense pas PostgreSQL.** Aucun point n'est associé à une base SQL. Les points vont au pipeline Spark, aux plans physiques, aux métriques. Ajouter PostgreSQL, c'est du travail et un service à maintenir pour zéro point.
- **PostgreSQL ajoute de la friction opérationnelle :** un serveur à lancer, un schéma à gérer, des connexions, une étape d'import depuis Parquet. Tout ça pour un bénéfice nul côté note.
- **DuckDB fait le même travail, en mieux, ici.** Si ton objectif est de pouvoir écrire des requêtes SQL sur tes résultats (par exemple pour alimenter un dashboard bonus), DuckDB lit **directement** les fichiers Parquet, sans serveur, sans import, sans compte. C'est l'outil pensé exactement pour ce cas : de l'analytique locale sur des fichiers.

**Quand PostgreSQL aurait du sens (pas ici) :** si le projet exigeait une vraie application transactionnelle avec des écritures concurrentes, des utilisateurs, des mises à jour ligne par ligne. Ce n'est pas le cas d'un pipeline analytique batch + streaming.

**Conclusion :** garde Parquet pour les couches bronze/silver/gold (c'est imposé). Si tu ajoutes un dashboard en bonus, mets **DuckDB** comme moteur de requête. Oublie PostgreSQL pour ce projet.

---

# 5. VERDICT — GitHub Archive est-il une bonne base de données pour ce projet ?

**Réponse courte : oui, c'est un excellent choix — sans doute l'un des meilleurs des quatre tracks proposés.**

**Pourquoi GitHub Archive convient parfaitement :**

- **C'est un track officiel.** Le professeur liste explicitement « Track B — Open Source (GitHub Archive) » parmi les quatre pistes autorisées. Aucun risque côté conformité.
- **Le volume est largement suffisant.** GitHub Archive publie des fichiers horaires de millions d'événements chacun. Quelques heures suffisent à dépasser le minimum de **10M de lignes / 3 Go** demandé, tout en restant gérable sur un laptop.
- **Il couvre les 5 composants du pipeline, ce qui est rare :**
  - *Batch ETL :* des événements JSON riches et imbriqués → parfait pour montrer bronze (brut) → silver (typé, aplati, contrats de schéma) → gold (tables analytics).
  - *Streaming :* les fichiers sont **déjà horaires** → idéal pour une « file source » : on les rejoue un par un dans un dossier `landing/`. C'est un cas d'usage streaming naturel, pas artificiel.
  - *Texte :* les données regorgent de champs textuels — messages de commit, titres et corps de PR, titres et corps d'issues, descriptions de releases → matière idéale pour un index inversé / TF-IDF.
  - *Itératif :* les données sont **intrinsèquement un graphe** (développeurs ↔ repos, forks, PR) → PageRank et connected components s'y appliquent naturellement. Et si tu préfères le clustering, on peut construire des features par repo (push, stars, forks, contributeurs).
  - *Préparation LLM :* les messages de commit et descriptions de PR forment un corpus texte réaliste à curer en `doc_id / text / metadata`.
- **C'est gratuit et public.** Les fichiers sont accessibles directement à `https://data.gharchive.org/` — **aucun compte, aucune clé API, aucun quota** (voir ci-dessous).
- **C'est valorisant pour un portfolio.** « Plateforme d'analyse de l'activité open-source mondiale » est un sujet parlant et concret pour un recruteur Data Engineering.

**Le seul point d'attention (déjà traité dans le prompt) :** ne pas télécharger massivement les archives. La bonne pratique — récupérer les fichiers horaires, les traiter en streaming, supprimer les fichiers temporaires — est intégrée dans `PROMPT_PROJET_DE2.md`, section « Stratégie GitHub Archive ».

**Faut-il un compte pour GitHub Archive ?** **Non.** Les fichiers horaires `.json.gz` sont des fichiers publics téléchargeables directement par URL. Tu n'as besoin ni de compte, ni de token, ni d'API GitHub. (À ne pas confondre avec l'**API REST de GitHub**, qui elle demande un token et impose des quotas — tu n'en as pas besoin ici.)

**Conclusion :** GitHub Archive est un très bon choix pour ce projet — riche, gratuit, sans compte, et il alimente naturellement les cinq composants exigés par le professeur.

---

# 6. Récapitulatif — par où commencer

1. **Installe le cœur :** conda + Java 21 + PySpark + JupyterLab. Vérifie que `spark.version` s'affiche.
2. **Récupère un fichier GitHub Archive de test** (une seule heure) et lis-le avec Spark.
3. **Suis `PROMPT_PROJET_DE2.md` phase par phase** — ne saute pas d'étape.
4. **Ne touche aux bonus** (Docker, Kafka, Quartz, dashboard, Cloudflare) **qu'une fois le cœur noté terminé** et le rapport rédigé.
5. **Comptes à créer :** uniquement **GitHub** (rendu + Actions) et, si tu fais le bonus déploiement, **Cloudflare** (ou GitHub Pages pour éviter une inscription). Tout le reste est local et sans compte.
