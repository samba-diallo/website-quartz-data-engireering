# 📊 ANALYSE APPROFONDIE DU PROJET DATA ENGINEERING

## 🎯 VUE D'ENSEMBLE

Ce projet est un **monorepo académique** pour les cours Data Engineering (S4) à ESIEE Paris, structuré comme un **site web statique** généré avec **Quartz v4.5.2** et déployé sur **Cloudflare Pages**.

---

## 📁 STRUCTURE PRINCIPALE

### 1️⃣ **content/** - SOURCE DE VÉRITÉ
Le cœur du projet contenant tout le contenu académique en Markdown :

#### **Data Engineering 1** (Spark, Hadoop, RDD/DataFrame)
- **3 Labs** avec practice + assignments :
  - Lab 1 : RDD vs DataFrame, transformations Spark
  - Lab 2 : Spark SQL, Data Warehouse, partitionnement
  - Lab 3 : Optimisations (broadcast joins, column pruning)
- **Projet final** : Pipeline ETL complet avec métriques
- Chaque lab contient :
  - Notebooks Jupyter (.ipynb) convertis en HTML
  - Documentation Markdown
  - Dossier `proof/` avec captures d'écran Spark UI
  - Fichiers de métriques et plans d'exécution

#### **Data Engineering 2** (Delta Lake, Lakehouse)
- **Lab 0** : Setup et configuration
- **Lab 2** : Index inversé, traitement PDF
- **Lab 3** : Clustering K-means avec MLlib
- Roadmap officielle en PDF
- **⚠️ MANQUANT** : Lab 1, projet final complet

---

### 2️⃣ **Data Engineering 1/** et **Data Engineering 2/** (racine)
Dossiers de **travail originaux** contenant :
- Notebooks sources avec outputs Spark
- Bases de données SQLite (`operational.db`)
- Outputs Parquet/CSV partitionnés
- Scripts Python (capture Spark UI, collecte métriques)
- Preuves d'exécution (screenshots, logs)

**Structure typique d'un lab** :
```
lab2-practice/
├── *.ipynb (notebooks)
├── *.py (scripts automation)
├── operational.db (données)
├── outputs/ (résultats Spark)
│   └── lab2/
│       ├── dim_*/  (tables dimension)
│       └── fact_sales/ (partitionné year/month)
└── proof/ (captures + plans)
```

---

### 3️⃣ **quartz/** - FRAMEWORK DE GÉNÉRATION
Quartz v4 (framework TypeScript/React) :
- **Components** : Layout, navigation, search, TOC
- **Plugins** : Transformers (Markdown→HTML), emitters (pages)
- **Static** : Assets statiques incluant notebooks HTML convertis
- Configuration : `quartz.config.ts`, `quartz.layout.ts`

---

### 4️⃣ **tools/** - SCRIPTS D'AUTOMATION
Scripts Bash pour automatiser le workflow :
- `notebook_to_quartz.sh` : Convertit .ipynb → HTML + génère wrapper iframe
- `generate_proof_index.sh` : Auto-génère index.md pour dossiers proof/

---

### 5️⃣ **migration/** - ARCHIVES
Backup de la Phase 1 de migration :
- Export du site original
- Archives tar.gz
- Documentation de migration

---

## 🔧 CONFIGURATION TECHNIQUE

### **Stack Technologique**
- **Framework** : Quartz v4.5.2 (SSG basé sur TypeScript)
- **Runtime** : Node.js ≥22, npm ≥10.9.2
- **Build** : esbuild + TypeScript
- **Déploiement** : Cloudflare Pages (auto-deploy sur push `main`)
- **Python** : venv `de1-env/` avec nbconvert pour notebooks

### **Git & Déploiement**
- **Remote** : `https://github.com/samba-diallo/website-quartz-data-engireering.git`
- **Branche locale** : `refactor/monorepo-architecture` (7 commits structurés)
- **⚠️ PAS ENCORE POUSSÉ** : Historiques divergents (local vs distant)
- **Cloudflare** : Écoute `origin/main` pour auto-deploy

---

## 📊 CONTENU ACADÉMIQUE DÉTAILLÉ

### **Data Engineering 1** ✅ COMPLET
| Composant | Statut | Contenu |
|-----------|--------|---------|
| Lab 1 Practice | ✅ | RDD vs DataFrame, starter notebook |
| Lab 1 Assignment | ✅ | Notebook + rapport + preuves Spark UI |
| Lab 2 Practice | ✅ | Spark SQL, Data Warehouse, scripts Python |
| Lab 2 Assignment | ✅ | Notebook + métriques + screenshots détaillés |
| Lab 3 Practice | ✅ | Optimisations Spark (broadcast, column pruning) |
| Lab 3 Assignment | ✅ | Notebook + analyse jobs Spark (9-12) |
| Projet Final | ✅ | Notebook + rapport + config YAML + 9 screenshots métriques |

### **Data Engineering 2** ⚠️ PARTIEL
| Composant | Statut | Contenu |
|-----------|--------|---------|
| Lab 0 Setup | ✅ | Configuration environnement |
| Lab 1 | ❌ | **MANQUANT** |
| Lab 2 Practice | ✅ | Index inversé, traitement PDF |
| Lab 3 Assignment | ✅ | K-means clustering, 8 partitions Parquet |
| Projet Final | ❌ | **ENTIÈREMENT MANQUANT** |
| Roadmap | ✅ | PDF officiel (4 pages) |

---

## 🎨 FONCTIONNALITÉS DU SITE

### **Navigation**
- Page d'accueil : Portail centralisé vers DE1, DE2, DevOps
- Index par cours avec tableaux labs/assignments
- Liens internes Obsidian-style `[[path|label]]`
- Breadcrumbs et table des matières

### **Notebooks Interactifs**
- Conversion .ipynb → HTML via nbconvert
- Intégration via iframes dans pages Markdown
- Préservation des outputs (graphiques, tableaux)

### **Preuves d'Exécution**
- Dossiers `proof/` auto-indexés
- Screenshots Spark UI (jobs, stages, SQL, métriques)
- Plans d'exécution physiques (.txt)
- Logs de métriques (.csv)

---

## ⚠️ POINTS D'ATTENTION

### **Contenu Manquant**
1. **DE2 Lab 1** : Practice + Assignment complets
2. **DE2 Projet Final** : Notebook, brief, checklist, rubric, rapport
3. **Support docs** : `node_support.md`, `oh-my-zsh_terminal_support.md`, `README_OptionA.md`
4. **DE1 Projet** : Brief détaillé, checklist, rubric (seuls notebook + rapport présents)

### **Git/Déploiement**
- **Historiques divergents** : Nécessite force-push ou PR avec résolution conflits
- **Branches** : `refactor/monorepo-architecture` pas encore mergée dans `main`
- **Cloudflare** : Déploiement en attente du push

### **Fichiers Lourds Exclus**
- `.gitignore` bien configuré pour exclure :
  - `node_modules/` (446 MB)
  - `de1-env/` (931 MB)
  - Outputs Spark régénérables
  - Caches Quartz

---

## 🚀 PROCHAINES ÉTAPES (selon NEXT_STEPS.md)

### **Phase 4 - Push GitHub** (À FAIRE)
**Option A** (recommandée) : Force-push comme nouvelle main
```bash
git branch -m refactor/monorepo-architecture main-new
git push origin main-new:main --force
```

**Option B** : Push comme branche + PR pour review

### **Phase 5 - Vérifier Cloudflare** (À FAIRE)
1. Vérifier build réussi sur dashboard Cloudflare
2. Tester site live : `https://website-quartz-data-engireering.pages.dev`
3. Valider chargement notebooks iframes
4. Vérifier accessibilité pages proof/

### **Phase 6 - Récupérer Contenu Manquant** (À FAIRE)
Contacter le prof pour obtenir :
- DE2 Lab 1 complet
- DE2 Projet final (5 fichiers)
- Support docs (3 fichiers)
- Briefs/checklists/rubrics manquants

---

## 💡 COMMANDES UTILES

```bash
# Build local
npx quartz build

# Dev server avec hot reload
npx quartz build --serve

# Convertir un notebook
PYTHON=de1-env/bin/python3 bash tools/notebook_to_quartz.sh "content/path/to/notebook.ipynb"

# Régénérer tous les proof/index.md
bash tools/generate_proof_index.sh

# Conversion batch de tous les notebooks
find content -name "*.ipynb" | while read nb; do
  PYTHON=de1-env/bin/python3 bash tools/notebook_to_quartz.sh "$nb"
done
```

---

## 📈 MÉTRIQUES DU PROJET

- **Fichiers totaux** : ~300+ (content + quartz + outputs)
- **Notebooks** : 15+ (.ipynb)
- **Screenshots** : 30+ (Spark UI)
- **Labs complets** : 6/7 (86%)
- **Projets finaux** : 1/2 (50%)
- **Taille repo** : ~2-3 GB (avec outputs, sans node_modules)

---

## ✅ POINTS FORTS

1. **Architecture propre** : Séparation claire content/framework/tools
2. **Documentation exhaustive** : PLAN.md, NEXT_STEPS.md, README détaillés
3. **Automation** : Scripts pour notebooks et proof indexes
4. **Preuves complètes** : Screenshots, métriques, plans d'exécution
5. **Déploiement moderne** : Cloudflare Pages avec CI/CD
6. **Versioning** : Git avec historique structuré (7 commits phases)

---

## 🔍 DÉTAILS TECHNIQUES SUPPLÉMENTAIRES

### **Arborescence Complète du Projet**
```
.
├── content/                          # Source de vérité Quartz
│   ├── index.md                      # Page d'accueil
│   ├── Data Engineering 1/
│   │   ├── index.md
│   │   ├── lab1 practice/
│   │   ├── lab1 assignment/
│   │   ├── lab2 practice/
│   │   ├── lab2 assignment/
│   │   ├── lab3 practice/
│   │   ├── lab3 assignment/
│   │   ├── project final/
│   │   └── support/
│   └── Data Engineering 2/
│       ├── index.md
│       ├── lab0 setup practice/
│       ├── lab2 practice/
│       ├── lab3 assignment/
│       └── roadmap-labs-project-DE2-FR.pdf
│
├── Data Engineering 1/               # Dossiers de travail originaux
│   ├── lab2-practice/
│   │   ├── *.ipynb
│   │   ├── *.py (scripts)
│   │   ├── operational.db
│   │   ├── outputs/
│   │   └── proof/
│   └── lab3-practice/
│
├── Data Engineering 2/
│   ├── lab0 setup practice/
│   ├── lab2 practice/
│   └── lab3 assignment/
│
├── quartz/                           # Framework Quartz v4
│   ├── components/
│   ├── plugins/
│   ├── static/
│   │   └── labs/                     # Notebooks HTML convertis
│   └── util/
│
├── tools/                            # Scripts automation
│   ├── notebook_to_quartz.sh
│   └── generate_proof_index.sh
│
├── migration/                        # Archives Phase 1
│
├── .github/                          # CI/CD (si configuré)
├── .claude/                          # Config Claude AI
├── .sixth/                           # Config additionnelle
│
├── quartz.config.ts                  # Config Quartz
├── quartz.layout.ts                  # Layout du site
├── package.json                      # Dépendances Node
├── tsconfig.json                     # Config TypeScript
├── .gitignore                        # Exclusions Git
├── NEXT_STEPS.md                     # Roadmap post-migration
└── recap.md                          # Ce fichier
```

### **Technologies et Versions**
- **Quartz** : v4.5.2
- **Node.js** : ≥22
- **npm** : ≥10.9.2
- **TypeScript** : v5.9.3
- **Python** : 3.x (dans de1-env/)
- **Spark** : Version utilisée dans les labs (à vérifier dans notebooks)
- **Delta Lake** : Pour DE2

### **Dépendances Principales (package.json)**
- **Build** : esbuild, typescript, sass
- **Markdown** : remark, rehype, unified
- **UI** : preact, d3, pixi.js
- **Math** : katex, mathjax
- **Code** : shiki (syntax highlighting)
- **Search** : flexsearch

---

## 🎓 CONTEXTE ACADÉMIQUE

### **Professeur Responsable**
Badr TAJINI - Cycle Data Engineering ESIEE Paris

### **Objectifs Pédagogiques**

#### **Data Engineering 1**
- Maîtriser Apache Spark (RDD, DataFrame, SQL)
- Comprendre le traitement distribué
- Optimiser les pipelines ETL
- Analyser les métriques Spark UI
- Implémenter un Data Warehouse

#### **Data Engineering 2**
- Découvrir l'architecture Lakehouse
- Utiliser Delta Lake (ACID, Time Travel)
- Traiter des données non structurées (PDF)
- Appliquer le Machine Learning distribué (MLlib)
- Construire des index inversés

### **Compétences Développées**
1. **Techniques** : Spark, Hadoop, SQL, Python, Git
2. **Architecturales** : Data Warehouse, Lakehouse, ETL
3. **Optimisation** : Partitionnement, broadcast joins, caching
4. **Monitoring** : Spark UI, métriques, plans d'exécution
5. **Documentation** : Notebooks, rapports, preuves

---

## 🛠️ WORKFLOW DE DÉVELOPPEMENT

### **Cycle de Travail Typique**
1. **Développement** : Coder dans notebooks Jupyter
2. **Exécution** : Lancer jobs Spark, collecter métriques
3. **Capture** : Screenshots Spark UI, sauvegarder plans
4. **Documentation** : Rédiger rapports Markdown
5. **Conversion** : `notebook_to_quartz.sh` pour HTML
6. **Build** : `npx quartz build` pour générer site
7. **Test** : `npx quartz build --serve` en local
8. **Deploy** : Push vers GitHub → Cloudflare auto-deploy

### **Scripts d'Automation**

#### **notebook_to_quartz.sh**
```bash
# Convertit .ipynb en HTML et crée wrapper iframe
PYTHON=de1-env/bin/python3 bash tools/notebook_to_quartz.sh \
  "content/Data Engineering 1/lab1 practice/DE1_Lab1_Notebook_EN.ipynb"
```

#### **generate_proof_index.sh**
```bash
# Auto-génère index.md pour tous les dossiers proof/
bash tools/generate_proof_index.sh
```

---

## 📦 OUTPUTS ET ARTEFACTS

### **Types de Fichiers Générés**

#### **Spark Outputs**
- **Parquet** : Tables dimension/fait partitionnées
- **CSV** : Statistiques agrégées
- **SQLite** : Bases opérationnelles
- **Checkpoints** : Points de reprise Spark

#### **Documentation**
- **HTML** : Notebooks convertis avec outputs
- **Markdown** : Rapports, index, documentation
- **PNG** : Screenshots Spark UI
- **TXT** : Plans d'exécution physiques
- **CSV** : Logs de métriques

#### **Configuration**
- **YAML** : Config projets (de1_project_config.yml)
- **JSON** : Métadonnées, configs
- **Python** : Scripts collecte métriques

---

## 🔐 SÉCURITÉ ET BONNES PRATIQUES

### **Fichiers Exclus du Git**
- ✅ Secrets et credentials (`.env`, `*.pem`, `*.key`)
- ✅ Environnements Python (`de1-env/`, `.venv/`)
- ✅ Node modules (`node_modules/`)
- ✅ Outputs régénérables (`outputs/`, `public/`)
- ✅ Caches (`.quartz-cache/`, `__pycache__/`)
- ✅ Fichiers système (`.DS_Store`, `Thumbs.db`)

### **Fichiers Inclus (Intentionnellement)**
- ✅ Notebooks HTML convertis (pour Quartz)
- ✅ Screenshots et preuves (documentation)
- ✅ Plans d'exécution (analyse)
- ✅ Métriques CSV (traçabilité)

---

## 🌐 DÉPLOIEMENT ET PRODUCTION

### **URL du Site**
- **Production** : `https://website-quartz-data-engireering.pages.dev`
- **Dev local** : `http://localhost:8080`

### **Configuration Cloudflare Pages**
- **Build command** : `npx quartz build`
- **Output directory** : `public/`
- **Branch** : `main`
- **Node version** : 22
- **Auto-deploy** : Activé sur push

### **Variables d'Environnement**
```typescript
// quartz.config.ts
const isProduction = process.env.NODE_ENV === "production"
const baseUrl = isProduction 
  ? "website-quartz-data-engireering.pages.dev"
  : "localhost:8080"
```

---

## 📝 HISTORIQUE DES PHASES

### **Phase 0** - Backup initial (commit cf5c83c)
Sauvegarde état initial avant refactoring

### **Phase 1** - Export + audit (commit 7921796)
Export contenu, analyse structure, identification toxiques

### **Phase 1.5** - Stratégie notebook prof (commit 9c7d8c6)
Décision approche notebooks (iframe vs conversion)

### **Phase 2** - Restructure content/ (commit c9061cf)
Réorganisation arborescence selon plan

### **Phase 2.5** - Quartz au root + verify build (commit 12eb908)
Installation Quartz, configuration, test build

### **Phase 2.6** - proof/ pages (commit e759dbf)
Génération automatique index proof/

### **Phase 3** - Cleanup website/ + remote (commit actuel)
Nettoyage, configuration Git remote

### **Phase 4** - Push GitHub (À FAIRE)
Synchronisation avec remote

### **Phase 5** - Vérifier Cloudflare deploy (À FAIRE)
Validation déploiement production

### **Phase 6** - Récupérer contenu manquant (À FAIRE)
Complétion DE2 et docs support

---

## 🎯 OBJECTIFS ATTEINTS

### ✅ **Architecture**
- [x] Monorepo structuré et maintenable
- [x] Séparation claire content/framework/tools
- [x] Documentation exhaustive
- [x] Scripts d'automation fonctionnels

### ✅ **Contenu DE1**
- [x] 3 labs complets (practice + assignment)
- [x] Projet final avec rapport
- [x] Preuves d'exécution complètes
- [x] Métriques et plans d'exécution

### ✅ **Technique**
- [x] Quartz v4 configuré et fonctionnel
- [x] Conversion notebooks automatisée
- [x] Build local validé
- [x] Git remote configuré

### ⚠️ **En Cours**
- [ ] Push vers GitHub
- [ ] Déploiement Cloudflare validé
- [ ] Contenu DE2 complet
- [ ] Support docs récupérés

---

## 🚨 ACTIONS PRIORITAIRES

### **Immédiat**
1. **Push GitHub** : Choisir stratégie (force-push ou PR)
2. **Valider Cloudflare** : Tester déploiement production
3. **Contacter prof** : Récupérer contenu manquant DE2

### **Court terme**
4. **Compléter DE2** : Ajouter Lab 1 et projet final
5. **Support docs** : Intégrer docs setup manquants
6. **Tests** : Valider tous les liens et iframes

### **Moyen terme**
7. **DevOps** : Ajouter contenu cours DevOps (mentionné mais absent)
8. **Ressources** : Compléter section ressources transverses
9. **CI/CD** : Configurer tests automatisés

---

## 💬 NOTES FINALES

### **Points Remarquables**
- Architecture très bien pensée et documentée
- Séparation propre entre sources et génération
- Automation intelligente (scripts, CI/CD)
- Preuves exhaustives (screenshots, métriques, plans)
- Git history structuré par phases

### **Améliorations Possibles**
- Ajouter tests automatisés (liens, builds)
- Documenter procédure ajout nouveau lab
- Créer template pour nouveaux cours
- Ajouter analytics (Google Analytics, Plausible)
- Implémenter recherche full-text

### **Recommandations**
1. **Backup** : Créer backup avant force-push
2. **Documentation** : Maintenir NEXT_STEPS.md à jour
3. **Versioning** : Utiliser tags Git pour releases
4. **Monitoring** : Surveiller métriques Cloudflare
5. **Maintenance** : Mettre à jour Quartz régulièrement

---

**Dernière mise à jour** : 2026-05-11  
**Auteur de l'analyse** : Claude (Assistant IA)  
**Version** : 1.0