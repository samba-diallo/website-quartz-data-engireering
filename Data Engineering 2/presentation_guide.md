# 📊 Guide d'Analyse & Présentation Finale : Plateforme E2E GitHub Analytics

Ce guide a été **mis à jour** pour s'aligner sur la stratégie de votre **Soutenance Finale (15 minutes)**. 

---

## 🎯 La Stratégie du Pivot Académique
Lors d'une soutenance de fin de projet (ESIEE Paris), le jury s'intéresse peu aux labs d'entraînement (que vous avez déjà validés ou présentés à mi-parcours). Il souhaite voir **la complexité du projet final**, la **rigueur scientifique** de vos optimisations physiques, et **les leçons apprises lors de la résolution de problèmes réels**.

**Notre approche** :
- **Labs 0 à 3** : Synthétisés sur **une seule slide ultra-rapide** (Slide 2) en début de présentation pour libérer du temps.
- **Plateforme E2E & Optimisations** : Représentent **80% du temps** et des slides.
- **Problèmes Techniques Réels** : Mis en avant avec fierté (Slide 6) pour montrer votre esprit critique et votre résilience d'ingénieur.
- **Preuves Visuelles** : Chaque diapositive technique intègre un fichier de preuve `.png` ou `.txt` du dossier `proof/`.

---

## 📐 1. Architecture Finale & Données

```
 ┌────────────────┐      ┌────────────┐      ┌──────────────┐
 │ GitHub Archive │ ───▶ │ Kafka Bus  │ ───▶ │ Spark Stream │
 │   (.json.gz)   │      │ (Ingestion)│      │  (Bronze)    │
 └────────────────┘      └────────────┘      └──────┬───────┘
                                                    │
 ┌────────────────┐      ┌────────────┐      ┌──────▼───────┐
 │ Next.js 16 UI  │ ◀─── │ FastAPI    │ ◀─── │ Airflow DAG  │
 │ (Lux de Minuit)│      │ + DuckDB   │      │(Silver/Gold) │
 └────────────────┘      └────────────┘      └──────────────┘
```

Vous avez déployé une architecture **Lakehouse Médaillon temps réel de production** :
- **Zookeeper & Kafka Broker (Port 9092)** : Buffer d'ingestion.
- **Custom Ingestion Producer** : Télécharge et "rejoue" l'activité dans le topic `github.raw.events`.
- **Spark Structured Streaming** : Ingestion Exactly-Once vers la couche Bronze Parquet.
- **Airflow Orchestrator (Port 8080)** : DAGs qui transforment la Bronze brute en Silver (typage, nettoyage) et Gold (agrégations par dépôt).
- **FastAPI Backend & DuckDB in-process (Port 8000)** : Requêtes sub-secondes sur les Parquets Gold.
- **Next.js 16 Dashboard (Port 3000)** : Visualiseur premium "Luxe de Minuit" (Sombre) / "Aurore" (Clair) avec switch de thèmes en 0.4s.

---

## 📸 2. Cartographie des Preuves Visuelles (`proof/`) par Slide

Pour prouver que votre code fonctionne réellement en production locale, projetez ces fichiers précis sur vos diapositives :

| Slide | Titre de la Slide | Fichier de Preuve à Projeter | Rôle Technique du Visuel |
| :--- | :--- | :--- | :--- |
| **Slide 2** | Les Fondations (Labs 0-3) | **`Executors.png`** (Spark UI) | Démontrer la validation initiale des exécuteurs et de l'environnement Spark. |
| **Slide 4** | Ingestion & Medallion | **`streaming_lastProgress.json`** <br>& **`plan_gold_query.txt`** | - Prouver la cadence et les watermarks stables du streaming. <br>- Démontrer le *Predicate Pushdown* sur la couche Gold Parquet. |
| **Slide 5** | NLP & Graphes PageRank | **`plan_iterative_pagerank.txt`** <br>& **`Jobs_Rankpage.png`** | - Prouver l'élimination physique du shuffle réseau par partitionnement de hachage. <br>- Montrer les jobs itératifs de calcul des rangs. |
| **Slide 6** | Problèmes & Solutions | **`Excutors_projetfinal.png`** | Montrer la charge mémoire stable des exécuteurs après résolution de l'OOM Silver (Column Pruning). |
| **Slide 8** | Démo Live & UI | **`Dashboard_DarkMode_LuxeDeMinuit.png`** <br>& **`Dashboard_LightMode_Aurore.png`** | - Présenter les dashboards premium sombre et clair (Switch en 0.4s). <br>- Montrer les métriques de production et le panneau "Pipeline Status". |

---

## 🎯 3. Déroulé des Slides & Scripts Oraux de Présentation

### Slide 1 : Titre & Storytelling (1 min)
*   **Titre** : Plateforme E2E GitHub Archive : De la Fondation Académique à l'Architecture de Production.
*   **Message Clé** : L'industrialisation d'une idée académique locale en une plateforme de données temps réel hautement optimisée et sécurisée.
*   **Contenu** : Présentation du binôme, du cours DE2 (ESIEE) et teasing de la stack complète.
*   **Script Oral** : 
    > *"Bonjour à tous. Lors de notre point de mi-parcours, nous vous avions présenté notre environnement de test et notre intention de concevoir une plateforme d'analyse des événements GitHub. Aujourd'hui, nous sommes fiers de vous présenter l'aboutissement final : une plateforme Lakehouse temps réel opérationnelle, sécurisée pour l'entreprise, capable de traiter plus de 10 millions de lignes en local, et dotée d'une interface décisionnelle sub-seconde."*

### Slide 2 : Les Fondations Validées (1 min)
*   **Titre** : Notre Parcours : Les Labs 0 à 3.
*   **Message Clé** : Les concepts fondamentaux (Batch Parquet, Structured Streaming, NLP, Clustering) ont été validés et consolidés durant la phase initiale.
*   **Contenu** :
    - **Lab 0** : Écriture Parquet partitionnée et comparaison des plans d'exécution.
    - **Lab 1** : Structured Streaming sur flux e-sport OpenDota (Watermarks de 5s).
    - **Lab 2** : Traitement NLP, pdfplumber et index inversé en cache mémoire.
    - **Lab 3** : Algorithme K-Means sur Spark MLlib et analyse de l'AdaptiveSparkPlan.
*   **Preuve Visuelle** : `Executors.png` (Spark UI validée).
*   **Script Oral** : 
    > *"Avant de plonger dans notre architecture finale, un rappel rapide de nos bases. À travers les quatre laboratoires imposés du programme, nous avons validé la manipulation de fichiers Parquet, les fenêtres temporelles de streaming, l'indexation de texte distribuée et le clustering K-Means avec l'AdaptiveSparkPlan. Ces jalons techniques sont validés, opérationnels, et ont servi de fondations pour notre plateforme finale."*

### Slide 3 : L'Architecture Globale de la Plateforme (2 min)
*   **Titre** : L'Écosystème Temps Réel E2E.
*   **Message Clé** : Une orchestration distribuée locale de 10 services via Docker Compose simulant fidèlement une architecture cloud d'entreprise.
*   **Contenu** :
    - **Ingestion** : Ingestion continue dans Kafka Broker via notre producteur Python custom.
    - **Calcul** : Consommation par Spark Structured Streaming, puis orchestration des DAGs batch par Apache Airflow.
    - **Serving** : FastAPI interrogeant les fichiers Parquet Gold via DuckDB (latence sub-100ms).
    - **Visualisation** : Interface Next.js 16 en thèmes "Luxe de Minuit" et "Aurore".
*   **Visuel** : Le schéma complet d'architecture de données (Kafka $\rightarrow$ Spark $\rightarrow$ Airflow $\rightarrow$ DuckDB $\rightarrow$ Next.js).
*   **Script Oral** : 
    > *"Pour notre architecture finale, nous avons dépassé le simple cadre du notebook. Nous avons conteneurisé un écosystème de 10 services sous Docker Compose. Un script Python pousse les événements GitHub compressés dans Apache Kafka pour simuler le temps réel. Spark Structured Streaming lit ce topic en continu pour stocker la couche Bronze. Apache Airflow prend ensuite le relais pour orchestrer nos transformations batch Silver et Gold. Le serving est assuré par FastAPI et le moteur SQL DuckDB, éliminant le besoin d'une base de données externe lourde."*

### Slide 4 : Le Cœur Ingestion, Streaming & Batch (2 min)
*   **Titre** : La Rigueur du Pipeline Medallion.
*   **Message Clé** : Un pipeline temps réel et batch structuré avec watermarks, assurant l'intégrité des schémas et le respect strict des SLOs de performance.
*   **Contenu** :
    - **Streaming** : File source Structured Streaming, watermark de 10 min, fenêtres de 5 min, mode `append` régulier.
    - **Medallion Batch** : Bronze brute, Silver partitionnée par date avec typage strict, Gold agrégée quotidiennement par dépôt (`repo_activity`).
    - **SLOs validés** : Ingestion Batch < 3 min (SLO < 10 min), Latence Trigger Streaming à 30s.
*   **Preuve Visuelle** : `streaming_lastProgress.json` (métriques de streaming en cours) et `plan_gold_query.txt` (Predicate Pushdown).
*   **Script Oral** : 
    > *"Le cœur de notre Lakehouse repose sur le modèle Médaillon. La couche Bronze stocke les événements bruts. La couche Silver les nettoie et applique des contrats de schéma. Enfin, la couche Gold calcule nos agrégations quotidiennes. Notre ingestion streaming utilise un Watermark de 10 minutes pour gérer l'arrivée de données en retard sans saturer la mémoire. Nos SLOs sont largement respectés : la transformation complète de millions de lignes prend moins de 3 minutes en local contre un objectif de 10 minutes."*

### Slide 5 : Analyse NLP & Graphes PageRank (2 min)
*   **Titre** : Algorithmes Avancés : NLP & PageRank.
*   **Message Clé** : L'analyse d'influence de l'écosystème GitHub par modélisation de graphes, optimisée physiquement pour éviter le shuffle réseau.
*   **Contenu** :
    - **NLP** : Index inversé distribué sur les messages de commits (`PushEvent`) pour un filtrage sub-seconde des termes clés (*fix, bug, feat*).
    - **Graphe PageRank** : Jointures PySpark itératives sur les relations Développeur $\rightarrow$ Dépôt.
    - **Optimisation physique** : Partitionnement par hachage explicite (`repartition(N, "src")`) pour colocaliser les nœuds et les arêtes, éliminant les coûteux *ShuffleExchangeExec* réseau entre les itérations.
*   **Preuve Visuelle** : `plan_iterative_pagerank.txt` (Élimination des shuffles après partitionnement) et `Jobs_Rankpage.png` (jobs itératifs).
*   **Script Oral** : 
    > *"Nous avons appliqué des analyses avancées sur nos données. Côté NLP, nous avons extrait les messages de commit pour créer un index inversé distribué permettant un filtrage instantané. Côté graphe, nous avons modélisé les contributions sous forme de relations Développeur-Dépôt et exécuté un algorithme de PageRank itératif. Face au coût important de shuffle réseau généré par les jointures successives de Spark, nous avons appliqué un repartitionnement par hachage sur la colonne source. Résultat visible sur notre plan d'exécution physique : les étapes de shuffle réseau ont été éliminées de nos itérations de calcul."*

### Slide 6 : Tempête sous un Crâne : Les Problèmes Rencontrés (3 min)
*   **Titre** : Résolution de Problèmes & Rigueur d'Ingénierie.
*   **Message Clé** : La réussite du projet réside dans notre capacité à identifier, investiguer et résoudre les anomalies techniques réelles.
*   **Contenu** :
    - **Java Heap Space OOM** : Résolu en remplaçant l'ingestion globale de l'énorme colonne `payload` par une sélection précoce et aplatie des attributs (gain de 95% de mémoire).
    - **Le Faux-Zéro (Active Devs)** : Un `try/except` silencieux masquait un fichier manquant dans FastAPI ; corrigé par des logs verbeux et la création du job Spark `user_activity`.
    - **CSS Turbopack (Erreur 837)** : L'inlining de Tailwind v4 imposait de placer Google Fonts en tête du fichier ; résolu en modifiant l'ordre des imports.
    - **Iframe Quartz** : Exclusion de routing pour préserver les extensions `.html` de nos rendus de notebooks.
*   **Preuve Visuelle** : `Excutors_projetfinal.png` (Spark UI démontrant la mémoire stable des exécuteurs).
*   **Script Oral** : 
    > *"Le développement en conditions réelles nous a confrontés à des obstacles enrichissants. Le plus grand défi a été une erreur OutOfMemory sur la couche Silver de Spark. En inspectant le schéma polymorphe de GitHub Archive, la JVM dépassait ses limites de mémoire. Nous avons implémenté un Column Pruning précoce, limitant la lecture aux seules colonnes nécessaires, ce qui a réduit l'empreinte mémoire de 95%. Nous avons également corrigé un faux-zéro sur l'API Next.js dû à un try/except silencieux masquant une table non générée, et résolu des problèmes subtils de cache CSS sous Tailwind v4 en réordonnant nos imports. Chaque problème a été résolu à la racine."*

### Slide 7 : DevOps, SecOps & Hardening (1 min)
*   **Titre** : Industrialisation & Sécurité (PR #18).
*   **Message Clé** : La protection du code et des accès est une priorité absolue, matérialisée par un audit SecOps complet et des workflows de CI/CD durcis.
*   **Contenu** :
    - **Audit de secrets** : Retrait des fichiers scratchs (`git rm --cached`) et externalisation des variables d'environnement (`.env` local et template `.env.example`).
    - **CI/CD Robuste** : Intégration de **gitleaks** (secret scanning) et de **CodeQL** (analyse de code statique) dans nos pipelines GitHub Actions.
    - **Branch protection** : Règles de validation de PR, CI verte obligatoire, et blocage des force-push sur la branche `main`.
*   **Visuel** : Icônes de sécurité GitHub et logs de la CI Actions au vert.
*   **Script Oral** : 
    > *"Un code performant doit être un code sûr. Nous avons mené un audit de sécurité complet lors de notre merge de branche final. Nous avons retiré les fichiers de brouillon temporaires de l'historique de suivi Git, externalisé tous nos mots de passe et credentials dans un fichier d'environnement local non commité, et configuré les outils gitleaks et CodeQL dans nos pipelines d'intégration continue. Notre branche principale est désormais protégée, bloquant toute fuite accidentelle de secret avant même son push."*

### Slide 8 : Démo : Le Dashboard "Luxe de Minuit" (2 min)
*   **Titre** : Serving de Données Analytiques & UI Cinématique.
*   **Message Clé** : L'exposition rapide et esthétique des résultats de calcul analytiques via un design system réactif à double thème.
*   **Contenu** :
    - **Vues UI** : Global Pulse, Data Sources, Kafka Streams, Spark Jobs, et guide utilisateur.
    - **Switch Thématique** : Mode sombre cinématique "Luxe de Minuit" et mode clair "Aurore" basculant en 0.4 seconde sans latence.
    - **Live Ingestion panel** : Indique en direct le nombre exact de fichiers Parquet détectés sur le disque par le backend.
*   **Preuve Visuelle** : `Dashboard_DarkMode_LuxeDeMinuit.png` et `Dashboard_LightMode_Aurore.png`.
*   **Script Oral** : 
    > *"Pour exposer ces statistiques à nos utilisateurs ou recruteurs, voici notre interface web. Elle interroge notre moteur DuckDB à travers notre API FastAPI toutes les 30 secondes. En direct, vous pouvez suivre les statistiques de commits, les parts d'événements, et l'activité par dépôt. Nous avons développé un double thème : un mode sombre par défaut inspiré des codes de l'industrie, et un mode clair Aurore, basculant instantanément en modifiant les variables CSS sous Tailwind v4. Un panneau de statut live en bas à gauche vérifie l'état d'activité de chaque couche du Lakehouse en lisant directement les métadonnées physiques."*

### Slide 9 : Bilan & Compétences (1 min)
*   **Titre** : Conclusion & Profil d'Ingénieur Data.
*   **Message Clé** : Ce projet final démontre une maîtrise complète du cycle de vie de la donnée, depuis l'ingestion brute jusqu'à la restitution optimisée et sécurisée.
*   **Contenu** :
    - **Compétences acquises** : Big Data (Spark, Kafka), Architecture (Medallion, Lakehouse), DevOps/SecOps (Airflow, Docker, CI/CD, Git hardening), Fullstack & Design (FastAPI, Next.js, Tailwind v4).
    - **Rapport technique final** : Rapport exhaustif de 8 pages rédigé et disponible sous [DE2_Project_Report.md](file:///home/sable/Documents/E4FD/S4/Data%20Engineering/Data%20Engineering%202/project%20final/DE2_Project_Report.md).
*   **Script Oral** : 
    > *"En conclusion, ce projet DE2 a été un véritable catalyseur. Il nous a permis d'acquérir des compétences d'ingénierie de données concrètes, applicables en entreprise : du tuning bas niveau de Spark à l'architecture d'ingestion Kafka, en passant par les pratiques rigoureuses de SecOps et de design d'interfaces. Notre pipeline est stable, nos SLOs sont validés et prouvés par des mesures concrètes. Nous sommes désormais pleinement outillés et prêts à relever des défis industriels complexes de Data Engineering. Nous remercions l'équipe pédagogique et sommes ouverts à vos questions."*
