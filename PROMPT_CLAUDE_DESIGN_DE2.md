# PROMPT POUR CLAUDE DESIGN - PRESENTATION DATA ENGINEERING 2

## CONTEXTE ET ROLE

Tu es un expert en design de presentations techniques avec 15 ans d'experience dans :
- les conferences tech internationales (AWS re:Invent, Google Cloud Next, Microsoft Build)
- le design storytelling pour presentations d'ingenierie
- le Data Engineering et les architectures Big Data
- les presentations DevOps et CI/CD modernes
- les presentations d'architecture logicielle
- les presentations startup et FAANG (Google, Meta, Amazon)

## OBJECTIF DE LA PRESENTATION

Creer une presentation PowerPoint premium de 10-15 minutes pour un professeur universitaire, demontrant l'avancement professionnel d'un projet Data Engineering 2 (DE2) axe sur :
- Lakehouse Architecture
- Delta Lake
- Apache Spark avance
- Structured Streaming
- Optimisations de performance
- Pipeline CI/CD moderne avec GitHub Actions et Cloudflare

## INFORMATIONS DU PROJET

### Contexte academique
- Cours : Data Engineering II (Workloads Intensifs en Donnees)
- Ecole : [NOM_ECOLE - A REMPLIR]
- Professeur : [NOM_PROFESSEUR - A REMPLIR]
- Binome : [MEMBRE_1 - A REMPLIR] et [MEMBRE_2 - A REMPLIR]
- Annee : 2025-2026

### Architecture globale du projet
Le projet utilise une stack moderne :
- VS Code (developpement local)
- GitHub Repository (versioning)
- GitHub Actions (CI/CD automatise)
- Quartz (generateur de site statique pour documentation)
- Cloudflare Pages (hebergement production)
- Site en production : website-quartz-data-engireering.pages.dev

## ANALYSE DETAILLEE DES LABS REALISES

### LAB 0 : Environment Validation & Setup Practice

**Objectif :** Valider l'environnement Spark et rafraichir les competences de lecture de plans d'execution.

**Technologies utilisees :**
- Apache Spark 4.0.0
- PySpark
- Parquet (format columnar)
- Spark UI pour monitoring

**Realisations techniques :**
1. Creation session Spark avec configuration locale
2. Lecture CSV avec schema explicite (StructType)
3. Ecriture Parquet partitionne par categorie
4. Comparaison des plans d'execution (CSV vs Parquet)
5. Capture de metriques Spark UI

**Preuves disponibles :**
- Screenshots Spark UI : Jobs_Lab0.png, Jobs1_lab0.png, Metrics.png
- Outputs Parquet partitionnes par categorie (business, science, tech)
- Plans d'execution compares

**Points techniques valorisants :**
- Utilisation de explain("formatted") pour analyse des plans
- Partitionnement intelligent des donnees
- Validation de l'environnement avant labs complexes

---

### LAB 1 : Structured Streaming Pipeline (Assignment)

**Objectif :** Implementer et optimiser un pipeline Structured Streaming pour evenements esport OpenDota avec agregation par fenetre temporelle.

**Piste de donnees :** Piste A (Esport/OpenDota)
- Schema : event_timestamp, team_id, hero_id, gold_earned, kills
- 2000 evenements synthetiques sur ~120 secondes
- Fenetre temporelle : 10 secondes
- Watermark : 5 secondes (tolerance pour donnees tardives)

**Architecture implementee :**

**Version Baseline (sans optimisation) :**
- Lecture du flux avec partition unique
- Agregation par fenetre sans repartitionnement
- Output : stream_sink_baseline (Parquet)
- Checkpoint : checkpoint_baseline

**Version Optimisee (avec repartitionnement) :**
- Lecture du flux + repartitionnement par team_id (4 partitions)
- Colocalisation des donnees d'equipe pour reduire shuffle
- Agregation par fenetre sur donnees repartitionnees
- Output : stream_sink_optimized (Parquet)
- Checkpoint : checkpoint_optimized

**Metriques capturees :**
- Plans d'execution (plan_baseline.txt, plan_optimized.txt)
- Nombre de lignes de sortie
- Statistiques d'agregation (avg event_count, avg total_gold)
- Verification des checkpoints pour exactly-once delivery
- Fichier CSV de comparaison : lab1_metrics_log.csv

**Preuves disponibles :**
- proof/plan_baseline.txt
- proof/plan_optimized.txt
- lab1_metrics_log.csv
- Outputs Parquet avec checkpoints

**Points techniques valorisants :**
- Structured Streaming avec watermarks
- Optimisation par repartitionnement strategique
- Garanties exactly-once via checkpoints
- Gestion des donnees tardives (late data)
- Comparaison baseline vs optimise avec metriques quantifiables

**Documentation technique :**
- ENGINEERING_NOTE.md : documentation complete de l'architecture
- GENAI.md : declaration d'absence d'utilisation d'IA generative (code 100% manuel)

---

### LAB 2 : Text Processing - Inverted Index Pipeline (Practice)

**Objectif :** Construire un pipeline de traitement de texte avec index inverse, tokenisation, normalisation et comparaison de formats de stockage.

**Technologies utilisees :**
- Apache Spark 4.0.0
- PySpark SQL et DataFrames
- pdfplumber (extraction texte PDF)
- Parquet vs CSV (comparaison performance)

**Pipeline technique :**

1. **Ingestion corpus de texte**
   - Lecture de documents PDF
   - Schema explicite : doc_id, text
   - Extraction et validation du contenu

2. **Tokenisation et normalisation**
   - Conversion en minuscules
   - Suppression caracteres speciaux (regex)
   - Split en tokens
   - Filtrage des stop words francais (assez, au, dans, de, etc.)

3. **Construction index inverse**
   - Explosion des tokens (explode)
   - GroupBy par token
   - Collecte des doc_ids par token
   - Calcul de frequence (count)
   - Tri par frequence decroissante

4. **Stockage et comparaison**
   - Ecriture Parquet : outputs/lab2/inverted_index
   - Ecriture CSV : outputs/lab2/inverted_index_csv
   - Mise en cache pour requetes rapides

5. **Mesure de latence des requetes**
   - Requetes sur tokens specifiques
   - Comparaison temps de reponse Parquet vs CSV
   - Capture metriques via lab2_metrics_log.csv

**Plans d'execution captures :**
- proof/plan_index_build.txt : plan de construction de l'index
  - AdaptiveSparkPlan avec 11 etapes
  - ObjectHashAggregate pour aggregation
  - Exchange (shuffle) avec hashpartitioning
  - Sort final par frequence
  
- proof/plan_query.txt : plan de requete sur l'index
  - InMemoryTableScan (donnees en cache)
  - Filter sur token specifique
  - Scan Parquet optimise avec Batched read

**Preuves disponibles :**
- Screenshots Spark UI : Job1.png, JOb2.png, Job3.png, Detailsjob.png, SQL.png
- Metriques : metrics1.png, metric2last.png
- Plans d'execution : plan_index_build.txt, plan_query.txt
- lab2_metrics_log.csv

**Points techniques valorisants :**
- Traitement de texte distribue a grande echelle
- Index inverse (technique fondamentale des moteurs de recherche)
- Optimisation avec mise en cache (InMemoryRelation)
- Comparaison formats columnar (Parquet) vs row-based (CSV)
- Plans d'execution complexes avec AdaptiveSparkPlan
- Filtrage intelligent des stop words

---

### LAB 3 : Advanced Analytics (Practice & Assignment)

**Objectif :** Analyses avancees avec Spark MLlib et optimisations de performance.

**Lab 3 Practice :**
- Notebook : DE2_Lab3_Notebook_EN.ipynb
- Preuves : jobs-Sql.png, jobs3.png, jobs4.png, jobs.png

**Lab 3 Assignment :**
- Notebook : assignment3_esiee.ipynb
- Clustering avec MLlib
- Outputs : cluster_assignments (Parquet partitionne en 8 fichiers)
- Metriques : lab3_metrics_log.csv
- Preuves : metric1.png, jobSpark.png

**Points techniques valorisants :**
- Machine Learning distribue avec Spark MLlib
- Clustering et assignation de clusters
- Partitionnement intelligent des resultats
- Optimisations de performance avancees

---

## PIPELINE CI/CD ET DEPLOIEMENT

### Architecture DevOps moderne

**Workflow complet :**
```
VS Code (developpement local)
    ↓
GitHub Repository (push vers main)
    ↓
GitHub Actions (CI/CD automatique)
    ↓
Build Quartz (generation site statique)
    ↓
Cloudflare Pages (deploiement production)
    ↓
Site en production (website-quartz-data-engireering.pages.dev)
```

### GitHub Actions - Workflow deploy.yml

**Declencheurs :**
- Push vers branche main
- Workflow manuel (workflow_dispatch)

**Etapes du pipeline :**

1. **Checkout repository**
   - Action : actions/checkout@v4
   - Recuperation du code source

2. **Setup Node.js**
   - Version : Node.js 22
   - Cache npm active pour performance
   - Action : actions/setup-node@v4

3. **Install dependencies**
   - Commande : npm ci (installation propre)
   - Utilisation du cache npm

4. **Build Quartz site**
   - Commande : npm run build
   - Environment : NODE_ENV=production
   - Generation du site statique dans /public

5. **Verify build artifacts**
   - Verification du contenu genere
   - Comptage des fichiers (minimum 10 requis)
   - Validation de l'integrite du build

6. **Deploy to Cloudflare Pages**
   - Action : cloudflare/pages-action@v1
   - Secrets utilises :
     - CLOUDFLARE_API_TOKEN
     - CLOUDFLARE_ACCOUNT_ID
   - Project : website-quartz-data-engireering
   - Directory : public

7. **Log deployment success**
   - Confirmation du deploiement reussi

### Configuration Quartz

**Fichier : quartz.config.ts**

**Configuration dynamique :**
- Base URL adaptative selon environnement
- Production : website-quartz-data-engireering.pages.dev
- Development : localhost:8080

**Caracteristiques :**
- Page title : "Data Engineering 1"
- Locale : fr-FR (francais)
- SPA enabled (Single Page Application)
- Popovers enabled
- Theme personnalise :
  - Fonts : Schibsted Grotesk (header), Source Sans Pro (body), IBM Plex Mono (code)
  - CDN caching active

**Structure du contenu :**
- Index principal : content/Data Engineering 2/index.md
- Organisation par labs (lab0, lab1, lab2, lab3)
- Liens internes avec syntaxe Obsidian
- Roadmap PDF reference

### Points techniques valorisants du deploiement

1. **Automatisation complete**
   - Zero intervention manuelle
   - Deploiement automatique sur push

2. **Pipeline moderne**
   - GitHub Actions (industrie standard)
   - Cloudflare Pages (edge computing)
   - Build verification automatique

3. **Performance**
   - Cache npm pour builds rapides
   - CDN Cloudflare global
   - Site statique ultra-rapide

4. **Fiabilite**
   - Verification des artifacts
   - Secrets securises
   - Logs de deploiement

5. **Documentation vivante**
   - Site Quartz genere automatiquement
   - Documentation toujours a jour
   - Accessible publiquement

---

## PREUVES ET CAPTURES D'ECRAN DISPONIBLES

### Lab 0
- Jobs_Lab0.png : Vue d'ensemble des jobs Spark
- Jobs1_lab0.png : Details d'un job specifique
- Metrics.png : Metriques de performance

### Lab 1
- plan_baseline.txt : Plan d'execution version baseline
- plan_optimized.txt : Plan d'execution version optimisee
- lab1_metrics_log.csv : Comparaison quantitative

### Lab 2
- Job1.png, JOb2.png, Job3.png : Progression des jobs
- Detailsjob.png : Details d'execution
- SQL.png : Vue SQL du plan
- metrics1.png, metric2last.png : Metriques de performance
- plan_index_build.txt : Plan de construction de l'index
- plan_query.txt : Plan de requete sur l'index

### Lab 3
- jobs-Sql.png, jobs3.png, jobs4.png, jobs.png : Jobs Spark UI
- metric1.png : Metriques de performance
- jobSpark.png : Details job Spark

---

## COMPETENCES TECHNIQUES ACQUISES

### Apache Spark avance
- Structured Streaming avec watermarks
- Optimisations de performance (repartitionnement)
- Plans d'execution et analyse de performance
- Formats columnar (Parquet) vs row-based (CSV)
- Mise en cache intelligente (InMemoryRelation)
- AdaptiveSparkPlan et optimisations automatiques

### Data Engineering moderne
- Pipeline de streaming temps reel
- Traitement de texte distribue
- Index inverse (moteurs de recherche)
- Machine Learning distribue (MLlib)
- Exactly-once delivery avec checkpoints
- Gestion des donnees tardives (late data)

### DevOps et CI/CD
- GitHub Actions pour automatisation
- Deploiement continu sur Cloudflare Pages
- Build verification automatique
- Gestion des secrets securisee
- Pipeline production-ready

### Documentation technique
- Site Quartz genere automatiquement
- Documentation vivante et accessible
- Notes d'ingenierie detaillees
- Declarations de methodologie (GENAI.md)

---

## INSTRUCTIONS POUR LA PRESENTATION

### Style visuel requis

**Design moderne et premium :**
- Minimaliste et epure
- Style engineering/tech conference
- Couleurs evoquant :
  - Data Engineering (bleus profonds, violets)
  - Cloud computing (bleus clairs, blancs)
  - Pipelines de donnees (gradients fluides)
  - Dashboards techniques (gris modernes, accents vifs)
  - Automatisation (verts technologiques)
  - DevOps moderne (oranges, bleus)

**Elements visuels :**
- Diagrammes professionnels de pipeline
- Fleches d'architecture modernes
- Blocs techniques avec ombres subtiles
- Animations visuelles intelligentes (transitions fluides)
- Icones modernes pour technologies
- Schemas de flux de donnees
- Graphiques de performance

**Typographie :**
- Titres : Police moderne sans-serif (Montserrat, Inter, ou similaire)
- Corps : Police lisible (Open Sans, Roboto)
- Code : Police monospace (Fira Code, JetBrains Mono)

### Structure de la presentation (10-15 minutes)

#### SLIDE 1 : Page d'accueil
**Contenu :**
- Titre : "Data Engineering 2 - Avancement du Projet"
- Sous-titre : "Lakehouse Architecture, Streaming & CI/CD Moderne"
- Informations :
  - Professeur : [NOM_PROFESSEUR - A REMPLIR]
  - Ecole : [NOM_ECOLE - A REMPLIR]
  - Matiere : Data Engineering II (Workloads Intensifs en Donnees)
  - Binome : [MEMBRE_1 - A REMPLIR] et [MEMBRE_2 - A REMPLIR]
  - Annee : 2025-2026

**Design :**
- Fond avec gradient subtil (bleu profond vers violet)
- Logo ecole (si disponible)
- Design epure et professionnel

**Timing :** 30 secondes

---

#### SLIDE 2 : Contexte et objectifs du cours
**Contenu :**
- Objectifs pedagogiques du cours DE2
- Technologies cibles : Lakehouse, Delta Lake, Spark avance
- Roadmap du professeur (reference au PDF)
- Etat actuel : Labs 0, 1, 2, 3 completes

**Visuel :**
- Timeline horizontale montrant progression
- Icones pour chaque technologie
- Indicateur de progression (ex: 60% complete)

**Timing :** 1 minute

---

#### SLIDE 3 : Architecture globale du projet
**Contenu :**
- Schema du pipeline complet :
  ```
  VS Code → GitHub → GitHub Actions → Quartz Build → Cloudflare → Production
  ```
- Technologies utilisees (avec logos) :
  - Apache Spark 4.0.0
  - PySpark
  - GitHub Actions
  - Quartz
  - Cloudflare Pages
  - Parquet, Delta Lake

**Visuel :**
- Diagramme de flux moderne avec fleches
- Icones/logos des technologies
- Couleurs distinctes par etape du pipeline

**Timing :** 1 minute 30

---

#### SLIDE 4 : Lab 0 - Environment Validation
**Contenu :**
- Objectif : Validation environnement Spark
- Technologies : Spark 4.0.0, Parquet
- Realisations :
  - Session Spark configuree
  - Lecture CSV avec schema explicite
  - Ecriture Parquet partitionne
  - Comparaison plans d'execution

**Visuel :**
- Screenshot : Jobs_Lab0.png ou Metrics.png
- Schema simple : CSV → Spark → Parquet
- Metriques cles en encadres

**Timing :** 1 minute

---

#### SLIDE 5 : Lab 1 - Structured Streaming (1/2)
**Contenu :**
- Objectif : Pipeline streaming temps reel
- Piste : Esport OpenDota (2000 evenements)
- Architecture :
  - Fenetre temporelle : 10 secondes
  - Watermark : 5 secondes
  - Exactly-once delivery via checkpoints

**Visuel :**
- Diagramme de streaming avec fenetre temporelle
- Representation visuelle du watermark
- Icones pour evenements esport

**Timing :** 1 minute 30

---

#### SLIDE 6 : Lab 1 - Structured Streaming (2/2)
**Contenu :**
- Comparaison Baseline vs Optimise
- Strategie d'optimisation : repartitionnement par team_id
- Resultats :
  - Reduction du shuffle
  - Meilleure colocalisation des donnees
  - Metriques quantifiables (lab1_metrics_log.csv)

**Visuel :**
- Tableau comparatif Baseline vs Optimise
- Graphique de performance (si metriques disponibles)
- Extrait du plan d'execution (simplifie)

**Timing :** 1 minute 30

---

#### SLIDE 7 : Lab 2 - Text Processing & Inverted Index (1/2)
**Contenu :**
- Objectif : Pipeline de traitement de texte
- Etapes :
  1. Ingestion corpus (PDF)
  2. Tokenisation et normalisation
  3. Filtrage stop words
  4. Construction index inverse

**Visuel :**
- Schema du pipeline de traitement
- Exemple de tokenisation visuelle
- Representation de l'index inverse (token → [doc_ids])

**Timing :** 1 minute 30

---

#### SLIDE 8 : Lab 2 - Text Processing & Inverted Index (2/2)
**Contenu :**
- Plans d'execution complexes :
  - AdaptiveSparkPlan (11 etapes)
  - ObjectHashAggregate
  - InMemoryTableScan (cache)
- Comparaison Parquet vs CSV
- Optimisations : mise en cache pour requetes rapides

**Visuel :**
- Screenshot : SQL.png ou Detailsjob.png
- Extrait du plan d'execution (simplifie et annote)
- Graphique comparatif Parquet vs CSV

**Timing :** 1 minute 30

---

#### SLIDE 9 : Lab 3 - Advanced Analytics
**Contenu :**
- Objectif : Analyses avancees avec MLlib
- Realisations :
  - Clustering distribue
  - Assignation de clusters
  - Optimisations de performance

**Visuel :**
- Screenshot : jobSpark.png ou metric1.png
- Schema de clustering visuel
- Metriques de performance

**Timing :** 1 minute

---

#### SLIDE 10 : Pipeline CI/CD - Architecture DevOps
**Contenu :**
- Workflow automatise complet
- GitHub Actions :
  - Checkout → Setup Node → Install deps → Build → Verify → Deploy
- Cloudflare Pages :
  - Deploiement automatique
  - CDN global
  - Site en production

**Visuel :**
- Diagramme de pipeline CI/CD moderne
- Logos GitHub Actions et Cloudflare
- Capture d'ecran du workflow (si disponible)
- URL du site en production

**Timing :** 2 minutes

---

#### SLIDE 11 : Demonstration des preuves
**Contenu :**
- Galerie de screenshots cles :
  - Spark UI (jobs, metriques)
  - Plans d'execution
  - Outputs Parquet
  - Site en production
- Validation technique du travail realise

**Visuel :**
- Grille de 4-6 screenshots
- Legende pour chaque capture
- Design type "portfolio engineering"

**Timing :** 1 minute 30

---

#### SLIDE 12 : Competences techniques acquises
**Contenu :**
- Apache Spark avance :
  - Structured Streaming, watermarks
  - Optimisations de performance
  - Plans d'execution
- Data Engineering moderne :
  - Pipelines temps reel
  - Index inverse
  - MLlib
- DevOps :
  - CI/CD avec GitHub Actions
  - Deploiement Cloudflare
  - Documentation automatisee

**Visuel :**
- 3 colonnes avec icones
- Puces concises
- Design type "skills matrix"

**Timing :** 1 minute

---

#### SLIDE 13 : Conclusion et prochaines etapes
**Contenu :**
- Etat actuel :
  - Labs 0, 1, 2, 3 completes
  - Pipeline CI/CD operationnel
  - Documentation en production
- Ce qui fonctionne :
  - Environnement Spark valide
  - Streaming optimise
  - Deploiement automatise
- Prochaines etapes :
  - Projet final DE2
  - Approfondissement Delta Lake
  - Time Travel et versioning

**Visuel :**
- Checklist avec coches vertes
- Timeline future
- Design positif et professionnel

**Timing :** 1 minute

---

#### SLIDE 14 : Questions et discussion
**Contenu :**
- "Questions ?"
- Contact ou informations complementaires

**Visuel :**
- Design minimaliste
- Icone de question stylisee
- Espace pour discussion

**Timing :** Variable (discussion)

---

## CONSIGNES IMPORTANTES

### A FAIRE ABSOLUMENT

1. **Utiliser les vrais noms de fichiers et dossiers**
   - lab0 setup practice, lab1 assignment, lab2 practice, lab3 assignment
   - outputs/lab1/stream_sink_baseline, outputs/lab1/stream_sink_optimized
   - proof/plan_baseline.txt, proof/plan_optimized.txt
   - website-quartz-data-engireering.pages.dev

2. **Ne rien inventer**
   - Utiliser uniquement les informations fournies dans ce prompt
   - Laisser des placeholders pour informations manquantes : [A REMPLIR]
   - Ne pas creer de fausses metriques ou resultats

3. **Construire un storytelling fluide**
   - Progression logique : validation → streaming → text processing → analytics → CI/CD
   - Transitions naturelles entre slides
   - Fil conducteur : evolution des competences techniques

4. **Proposer les meilleurs visuels possibles**
   - Diagrammes professionnels (style AWS/Google Cloud)
   - Schemas de pipeline modernes
   - Graphiques de performance elegants
   - Screenshots integres avec legenedes

5. **Produire une structure slide par slide**
   - Contenu detaille pour chaque slide
   - Suggestions visuelles precises
   - Timing approximatif par slide

6. **Ajouter des notes de presentation**
   - Points cles a mentionner oralement
   - Transitions entre slides
   - Elements a emphasiser

### STYLE ET QUALITE

- **Niveau de qualite :** Portfolio engineering premium
- **Reference :** Presentations AWS re:Invent, Google Cloud Next
- **Ton :** Professionnel, technique, mais accessible
- **Langage :** Francais (sauf termes techniques en anglais)

### LIVRABLES ATTENDUS

1. **Structure complete de la presentation**
   - Contenu detaille de chaque slide
   - Suggestions visuelles precises
   - Notes de presentation

2. **Specifications de design**
   - Palette de couleurs
   - Typographie
   - Style des diagrammes

3. **Assets a creer**
   - Liste des diagrammes necessaires
   - Liste des graphiques a generer
   - Screenshots a integrer

4. **Timing et transitions**
   - Duree par slide
   - Points de transition
   - Rythme de presentation

---

## INFORMATIONS COMPLEMENTAIRES

### Fichiers et artefacts disponibles

**Lab 0 :**
- DE2_Lab0_Starter.ipynb
- data/sample.csv
- outputs/lab0/sample_parquet/ (partitionne par category)
- Proof/Jobs_Lab0.png, Jobs1_lab0.png, Metrics.png

**Lab 1 :**
- assignment1_esiee.ipynb
- ENGINEERING_NOTE.md
- GENAI.md
- data/opendota_events.csv
- outputs/lab1/stream_sink_baseline/
- outputs/lab1/stream_sink_optimized/
- outputs/lab1/checkpoint_baseline/
- outputs/lab1/checkpoint_optimized/
- proof/plan_baseline.txt
- proof/plan_optimized.txt
- lab1_metrics_log.csv

**Lab 2 :**
- DE2_Lab2_Notebook_EN.ipynb
- data/pdfs/ (doc1.pdf, doc2.pdf, doc3.pdf)
- outputs/lab2/inverted_index/ (Parquet)
- outputs/lab2/inverted_index_csv/ (CSV)
- proof/Job1.png, JOb2.png, Job3.png, Detailsjob.png, SQL.png
- proof/metrics1.png, metric2last.png
- proof/plan_index_build.txt, plan_query.txt
- lab2_metrics_log.csv

**Lab 3 :**
- DE2_Lab3_Notebook_EN.ipynb (practice)
- assignment3_esiee.ipynb (assignment)
- outputs/lab3/cluster_assignments/ (8 fichiers Parquet)
- proof/jobs-Sql.png, jobs3.png, jobs4.png, jobs.png
- proof/metric1.png, jobSpark.png
- lab3_metrics_log.csv

**CI/CD :**
- .github/workflows/deploy.yml
- quartz.config.ts
- content/Data Engineering 2/index.md
- Site production : website-quartz-data-engireering.pages.dev

### Technologies et versions
- Apache Spark : 4.0.0
- Node.js : 22
- Python : 3.x (avec PySpark)
- GitHub Actions : actions/checkout@v4, actions/setup-node@v4, cloudflare/pages-action@v1

---

## DEBUT DE LA CREATION

Cree maintenant une presentation PowerPoint exceptionnelle qui :
1. Respecte toutes les consignes ci-dessus
2. Utilise un design moderne et professionnel
3. Raconte une histoire technique coherente
4. Met en valeur le travail realise
5. Impressionne le professeur par la qualite technique et visuelle

La presentation doit etre digne d'une conference tech internationale tout en restant adaptee au contexte academique.

Commence par proposer la structure complete avec le contenu detaille de chaque slide, puis les specifications de design.