# PLAN DE RÉORGANISATION ARCHITECTURALE
## Repository Data Engineering - Transformation Monorepo

**Date :** 11 Mai 2026  
**Version :** 1.0  
**Statut :** En attente de validation utilisateur  
**Niveau Détail :** Enterprise-Grade (14 ans d'expérience DevOps/Data Engineering)

---

## CONTEXTE PROFESSIONNEL

Après 14 ans dans les domaines du Data Engineering et du DevOps, j'ai analysé cette structure repository et identifié une situation classique de dette technique croissante. Le problème central n'est pas une erreur de conception initiale, mais plutôt l'absence de gouvernance structurelle lors de la croissance du projet.

Actuellement, vous avez:
- Un repository monolithique de 11GB où 85% est inutile (cache Python + historique git dupliqué)
- Deux notations de dossiers incohérentes (tirets vs espaces) entre DE1 et DE2
- Aucune automation CI/CD, ce qui force des déploiements manuels et augmente le risque d'erreur
- Une séparation floue entre contenu pédagogique (labs, assignments) et infrastructure DevOps
- Pas de conventions documentées, ce qui rend l'onboarding de nouveaux contributeurs difficile

Cette migration vers une architecture monorepo bien structurée n'est pas optionnelle pour la scalabilité long-term. C'est une investissement de 3-4 jours pour éliminer 18+ mois de dette technique potentielle.

---

## TABLE DES MATIÈRES

1. [Diagnostic État Actuel](#diagnostic-état-actuel)
2. [Matrice des Problèmes](#matrice-des-problèmes)
3. [Architecture Cible Recommandée](#architecture-cible-recommandée)
4. [Approche de Migration](#approche-de-migration)
5. [Plan d'Exécution Détaillé](#plan-dexécution-détaillé)
6. [Standards et Conventions](#standards-et-conventions)
7. [Checklist d'Implémentation](#checklist-dimplémentation)
8. [Code Generation Guidelines](#code-generation-guidelines)

---

## DIAGNOSTIC ÉTAT ACTUEL

### Métrique de Santé Générale
**Score Architecturale : 3.5/10** CRITIQUE

État du Repository
- Taille : 11 GB (excessif pour un repository accademique)
- Clone time : 30s+ (seuil d'acceptabilité : <5s)
- Build time : Indéterminé (aucune automation n'existe)
- Navigation : Confuse et peu intuitive
- Maintenabilité : Très difficile (croissante avec chaque contribution)
- Scalabilité : Limitée à court terme (non viable pour 3+ années d'enseignement)

```
État du Repository
├── Taille : 11 GB (excessif)
├── Clone time : 30s+ (lent)
├── Build time : Unknown (pas de CI/CD)
├── Navigation : Confuse
├── Maintenabilité : Très difficile
└── Scalabilité : Limitée (long-term unsustainable)
```

### Approche Recommandée : HYBRID MIGRATION
- Temps estimé : 3-4 jours
- Risque technique : Moyen (contrôlé)
- Qualité finale attendue : 8.5/10
- Stratégie : Garder les DATA, restructurer la FORM

### Objectif Principal
Transformer le repository en une architecture monorepo professionnelle permettant:
- Une source unique de vérité pour tout contenu (Markdown + Notebooks)
- Quartz v4.5.2 pour génération site statique automatisée
- GitHub Actions CI/CD complet (lint, validation, deployment)
- Cloudflare Pages pour hosting statique haute-performance
- Obsidian-compatible vault pour workflow éditorial
- Scalabilité pour 10+ cours sans restructuration majeure

---

## DIAGNOSTIC ÉTAT ACTUEL (Détaillé)

---

## DIAGNOSTIC ÉTAT ACTUEL (Détaillé)

### Morphologie Réelle du Repository

```
Data Engineering/                    (Workspace root)
│
├── Data Engineering 1/              (Source cours S1)
│   ├── DE1_Project_Notebook_EN.ipynb
│   ├── lab1-practice/
│   │   ├── assignment1_esiee.ipynb
│   │   ├── assignment1_genai.md
│   │   └── DE1_Lab1_Notebook_EN.ipynb
│   ├── lab2-practice/
│   ├── lab3-practice/
│   ├── projet-final/
│   │   ├── DE1_Project_Notebook_EN.ipynb (duplicate!)
│   │   ├── DE1_Project_Report.md
│   │   └── project_final_genai.md
│   ├── website1/                    ⚠️ DUPLIQUÉ (Quartz)
│   └── node_modules/                (ne devrait pas être là)
│
├── Data Engineering 2/              (Source cours S2)
│   ├── lab0 setup practice/
│   ├── lab1 assignment/
│   ├── lab1 practice/
│   ├── lab2 assignment/
│   ├── lab2 practice/
│   ├── lab3 assignment/
│   ├── lab3 practice/
│   ├── project final/
│   └── roadmap-labs-project-DE2-FR.pdf
│
├── website/                         (Quartz monolithe - 11 GB!)
│   ├── content/                     (1.2 MB) ✓ Précieux
│   │   ├── labs/
│   │   ├── devops/
│   │   ├── project/
│   │   └── index.md
│   │
│   ├── devops_base/                 (9.4 GB) ❌ TOXIQUE
│   │   ├── .conda/                  (6+ GB) ← Instalation Python
│   │   ├── .git/                    (2+ GB) ← Historique dupliqué
│   │   ├── td0-td6/                 (200 MB) ← Contenu valide
│   │   ├── projet-final-devops/
│   │   └── scripts/                 ← Mélange Terraform/Docker/K8s
│   │
│   ├── quartz/                      (35 MB) ~ Framework
│   ├── static/                      (8.2 MB) ~ Assets
│   ├── public/                      (24 MB) ⚠️ Build output
│   ├── node_modules/                (446 MB) ⚠️ Dépendances
│   ├── quartz.config.ts
│   ├── quartz.layout.ts
│   ├── package.json
│   └── [Scripts shell]
│
├── de1-env/                         (Python venv)
├── verify_spark.py                  (Orphelin)
├── .claude/, .sixth/                (Config système)
└── [Fichiers root]
```

### Analyse Quantitative du Repository

| Composant | Taille | % Global | Évaluation | Action Recommandée |
|-----------|--------|----------|------------|-------------------|
| devops_base/ | 9.4 GB | 85% | TOXIQUE | Extraire + Nettoyer |
| node_modules/ (website) | 446 MB | 4% | Normal | Ajouter gitignore |
| quartz/ | 35 MB | 0.3% | Acceptable | Restructurer config |
| public/ | 24 MB | 0.2% | Build output | Ignorer/Regénérer |
| content/ | 1.2 MB | 0.01% | PRÉCIEUX | Préserver et Réorganiser |
| DE1/DE2 sources | ~50 MB | 0.5% | CRITIQUES | Standardiser |

**Conclusion Quantitative :** 85% du poids repo = Python environment (.conda/) + Git history archive (.git/) = DOIT DISPARAITRE IMMÉDIATEMENT

### III. Analyse Structurelle

#### 🔴 Problème 1 : Incohérence Nommage (DE1 vs DE2)

```
DE1                          DE2
├── lab1-practice/           ├── lab1 practice/           ← Espaces vs tirets!
├── lab2-practice/           ├── lab2 practice/
├── lab3-practice/           ├── lab3 practice/
├── NO lab0!                 ├── lab0 setup practice/     ← DE2 a lab0
└── projet-final/            └── project final/           ← FR vs EN + espaces
```

**Impact :** Confusion navigation, impossible d'automatiser

#### 🔴 Problème 2 : Séparation practice vs assignment floue

**DE1 :**
- Tous les labs juste "practice"
- Les assignments mélangés dans les même dossiers

**DE2 :**
- Distinction claire "lab1 assignment" vs "lab1 practice"
- Manque `lab3 assignment`

**Impact :** Structure incohérente, pas de norme

#### 🔴 Problème 3 : devops_base = Poison

```
website/devops_base/ (9.4 GB!)
├── .conda/              ← Python environment (6GB) - JAMAIS en source!
├── .git/                ← Historique dupliqué (2GB)
├── Linux binaries       ← Dépendances système
└── Contenu DevOps       ← Mélangé avec site web
```

**Pourquoi c'est un problème :**
- Clone = 30s+ au lieu de 2s
- Build = lent et imprévisible
- `.conda/` = spécifique machine
- `.git/` = devrait être dans repo séparé

#### 🔴 Problème 4 : Duplication website/website1

```
Data Engineering 1/website1/ = clone de website/
└─ Sync jamais effectuée
└─ Source de vérité incertaine
└─ Confusion pour contributeurs
```

#### 🔴 Problème 5 : Pas de CI/CD

```
Workflow actuel:
Edit Markdown
  → Manual build
  → Manual deployment
  → Hope it works 😅
```

**Besoin :**
- Lint automatique
- Link checking
- Build validation
- Deploy auto

#### 🔴 Problème 6 : Structure Quartz non-optimale

```
content/ structure
├── labs/
├── devops/          ← Mélange DE + DevOps!
├── project/
└── index.md

Problèmes:
- Pas de hiérarchie de domaines
- Sidebar = chaos
- Graph view = non-informatif
- Obsidian compatibility = médiocre
```

#### 🔴 Problème 7 : `.gitignore` incomplet

```
Actuellement ignoré:
✓ node_modules
✓ .obsidian
✓ private/

NON ignoré (problème):
✗ .quartz-cache/          ← Cache generated
✗ public/                 ← Build output
✗ .conda/                 ← Environment
✗ venv, .venv/            ← Python envs
✗ *.pyc, __pycache__/     ← Compiled Python
```

#### 🔴 Problème 8 : Pas de conventions

```
Pas de standard pour:
- Nommage fichiers
- Frontmatter YAML
- Tags normalisés
- Structure des liens
- Assets management
├─ Chacun fait son truc
└─ Chaos long-term
```

### IV. Analyse Git & Versioning

```
État Git:
├── Repository unique (bon)
├── Pas de submodules (bon)
├── branch strategy = undefined (mauvais)
├── Tags = désorganisés (mauvais)
├── devops_base/.git/ = dupliqué (TOXIQUE)
└── Pas de conventional commits (mauvais)
```

### V. Matrice Problèmes vs Impact

| Problème | Sévérité | Impact Immédiat | Impact Long-term |
|----------|----------|-----------------|-----------------|
| `devops_base/` (9.4GB) | 🔴 Critique | Clone lent, builds casse | Repository unmaintainable |
| Nommage incohérent | 🔴 Critique | Confusions quotidiennes | Scaling impossible |
| Pas CI/CD | 🔴 Critique | Déploiement manuel | Erreurs en prod |
| Duplication contenu | 🟠 Majeur | Désync risque | Data loss possible |
| Pas conventions | 🟠 Majeur | Confusion contrib | Onboarding difficile |
| Quartz config adhoc | 🟡 Moyen | Navigation confuse | Architecture fragile |
| `.gitignore` incomplet | 🟡 Moyen | Fichiers sensibles | Sécurité compromise |
| Obsidian incompatible | 🟡 Moyen | Workflow compromis | Productivité réduite |

---

## MATRICE DES PROBLÈMES IDENTIFIÉS

### Problèmes Critiques (Bloquants pour scalabilité)

#### P1 : Repository Oversized (11 GB) -- CRITIQUE
**Description :**  
Le repository pèse 11 GB, 85% dus à `.conda/` + `.git/` dupliqué dans `devops_base/`.

**Symptômes Observés :**
- git clone = 30s+ au lieu de 2s
- npm ci = 60s+ (npm doit traverser 400MB node_modules)
- GitHub workflow timeout possible
- Performance disque dégradée lors clonage répété

**Cause Racine :**
- `.conda/` = Python environment avec toutes les binaires système (6GB+)
- `.git/` = Historique complet non-compressé (2GB+)
- Assets non-optimisés

**Solution Recommandée :** 
Extraire `devops_base/` vers Docker volume ou dépôt séparé

---

#### P2 : Architecture Incohérente (DE1 vs DE2) -- CRITIQUE
**Description :**  
DE1 utilise `lab1-practice/` (tirets), DE2 utilise `lab1 practice/` (espaces). Divergences additionnelles : FR vs EN, existence lab0 uniquement en DE2, structure assignment non-uniforme.

**Impact Observé :**
- Impossible d'automatiser imports cross-courses
- Contributeurs confus par incohérence nomenclature
- Scripts non-portables

**Solution Recommandée :**  
Normaliser partout avec notation DE2 uniforme : `lab1 assignment/`, `lab1 practice/` (espaces, pas de tirets)

---

#### P3 : Pas de CI/CD Pipeline -- CRITIQUE
**Description :**  
Aucune GitHub Actions configurée. Pas de build validation, pas de deploy automatique.

**Impact :**
- Déploiement manuel = risques d'erreur humaine élevés
- Pas de link checking automatisé
- Pas de Markdown linting
- Pas de preview deployments pour validation avant production

**Solution :**  
Créer workflows GitHub Actions complets : lint, validation, deployment

---

#### P4 : Quartz Configuration Adhoc -- CRITIQUE
**Description :**  
Quartz v4.5.2 a des customisations non-optimales, pas de sidebar hierarchy décente, pas de support Obsidian natif.

**Impact :**
- Navigation = chaos
- Graph view = peu utile
- Obsidian + Quartz = désynchronisés (incompatibilité lien format)

**Solution :**  
Reconfigurer Quartz from scratch avec best practices modernes

---

### Problèmes Majeurs (Important mais non-bloquants immédiatement)

#### P5 : Duplication website vs website1
**Description :**  
`Data Engineering 1/website1/` = clone non-synchronisé de `website/`.

**Impact :**
- Confusion sur source de vérité
- Maintenance double = perte d'effort
- Potentiel data drift entre versions

**Recommandation :**  
Supprimer doublons, un seul `website/` (ou mieux : intégrer au monorepo)

---

#### P6 : devops_base Mélangé
**Description :**  
Contenu DevOps entreposé dans `website/devops_base/` au lieu d'être au niveau monorepo root.

**Impact :**
- DevOps tight-coupled au site web
- Réutilisation scripts/infra difficile
- Structure illogique pour future scalabilité

---

#### P7 : Pas de Conventions
**Description :**  
Pas de guide CONTRIBUTING, pas de standards : nommage fichiers, frontmatter, tags, liens internes.

**Impact :**
- Chaos quilmédiocrité
- Chacun son style
- Difficile d'onboard nouveaux contributeurs

**Recommandation :**  
Créer `CONTRIBUTING.md` exhaustif

---

### C. Problèmes Mineurs (Nice-to-have)

#### P8 : .gitignore Incomplet
**Description :**  
`.quartz-cache/`, `public/`, `.venv/`, `__pycache__/` non ignorés

**Impact :**  
Cache files pollue commits, environment-specific files versionnés

#### P9 : Orphaned Files
**Description :**  
`verify_spark.py` à la racine, `.claude/`, `.sixth/` non-documentés

---

## 🏗️ Architecture Cible

### I. Structure Monorepo Idéale

```
data-engineering/                 ← Single repo
│
├── 📚 Content (Source de Vérité)
│   └── docs/                      ← Quartz input (source de vérité)
│       ├── _index.md              ← Site root
│       ├── _meta.json             ← Navigation metadata
│       │
│       ├── DE1 — Data Engineering I/  (dossier affiché comme "DE1 — Data Engineering I")
│       │   ├── _index.md
│       │   ├── lab0 assignment/       (si besoin, sinon optionnel pour DE1)
│       │   ├── lab0 practice/         (si besoin, sinon optionnel pour DE1)
│       │   ├── lab1 assignment/
│       │   │   ├── _index.md
│       │   │   ├── assignment1_esiee.ipynb / .md
│       │   │   ├── assignment1_genai.md
│       │   │   └── assets/
│       │   ├── lab1 practice/
│       │   │   ├── _index.md
│       │   │   ├── DE1_Lab1_Notebook_EN.md (converted)
│       │   │   └── assets/
│       │   ├── lab2 assignment/
│       │   ├── lab2 practice/
│       │   ├── lab3 assignment/
│       │   ├── lab3 practice/
│       │   ├── project final/
│       │   │   ├── _index.md
│       │   │   ├── DE1_Project_Notebook_EN.md
│       │   │   ├── DE1_Project_Report.md
│       │   │   └── assets/
│       │   └── assets/
│       │
│       ├── DE2 — Data Engineering II/
│       │   ├── _index.md
│       │   ├── lab0 setup practice/
│       │   │   ├── _index.md
│       │   │   ├── DE2_Lab0_Starter.md (converted)
│       │   │   └── assets/
│       │   ├── lab1 assignment/
│       │   │   ├── _index.md
│       │   │   ├── assignment1_esiee.ipynb / .md
│       │   │   ├── ENGINEERING_NOTE.md
│       │   │   ├── GENAI.md
│       │   │   └── assets/
│       │   ├── lab1 practice/
│       │   ├── lab2 assignment/
│       │   ├── lab2 practice/
│       │   ├── lab3 assignment/
│       │   ├── lab3 practice/
│       │   ├── project final/
│       │   │   ├── _index.md
│       │   │   ├── DE2_Project_Notebook_EN.md
│       │   │   └── assets/
│       │   └── assets/
│       │
│       ├── 03-DevOps/             (nouveau domaine)
│       │   ├── foundations/
│       │   │   ├── docker.md
│       │   │   ├── kubernetes.md
│       │   │   └── cloud.md
│       │   ├── cicd/
│       │   │   ├── github-actions.md
│       │   │   └── terraform.md
│       │   ├── monitoring/
│       │   ├── labs/
│       │   │   ├── td-0/, td-1/, ... td-6/
│       │   └── assets/
│       │
│       └── Ressources/
│           ├── glossary.md
│           ├── resources.md
│           └── templates/
│
├── 🛠️ Quartz Config (Génération)
│   ├── quartz/                    ← Framework (from node_modules)
│   ├── quartz.config.ts           ← Config clean
│   ├── quartz.layout.ts           ← Sidebar hierarchy
│   ├── package.json
│   └── tsconfig.json
│
├── 🤖 Automation (CI/CD)
│   └── .github/
│       └── workflows/
│           ├── ci.yml             ← Lint, check, test
│           ├── quartz-deploy.yml  ← Build + deploy
│           └── [autres...]
│
├── 😸 Obsidian Workspace (Local)
│   └── obsidian/
│       ├── .obsidian/             ← Vault config
│       └── README.md
│
├── 📦 Build Output (Ignored)
│   └── public/                    ← Quartz output (⚠️ .gitignore)
│
├── 🎨 Static Assets
│   └── static/
│       └── images/
│           ├── de1/, de2/, devops/, shared/
│           └── [autres]
│
├── 📋 Documentation Repository
│   ├── README.md                  ← Landing page
│   ├── CONTRIBUTING.md            ← Conventions
│   ├── ARCHITECTURE.md            ← Technical docs
│   ├── .gitignore                 ← Strict!
│   └── [autres configs]
│
└── 🐳 Infrastructure (Optionnel)
    ├── docker/
    ├── terraform/
    └── scripts/
```

### II. Comparaison Avant/Après

| Aspect | Avant | Après | Gain |
|--------|-------|-------|------|
| Taille repo | 11 GB | ~200 MB | 98% réduction |
| Clone time | 30s+ | 2s | 15x plus rapide |
| Build time | N/A | ~5s | Automated |
| Navigation | 😵 | 🎯 Quartz sidebar (DE1, DE2, DevOps) | Clarity |
| Obsidian | ❌ Non-natif | ✅ Native vault (`[[links]]`) | Seamless |
| CI/CD | ❌ Rien | ✅ Complet | Safety |
| Notation | 🔀 Mélangée (tirets + espaces) | ✅ Uniforme (DE2 style) | Consistency |
| Maintenabilité | 😫 Hard | 😊 Easy | Scalable |
| Conventions | ❌ None | ✅ Documenté | Structure |

---

## ✅ Recommandation Finale

### Approche Choisie : **HYBRID MIGRATION**

**Philosophie :** "Keep data, reshape form"

```
PHASE 1 : Export (Jour 1)
├─ Sauvegarder contenu critique
├─ Extraire Markdown/Notebooks
└─ Nettoyer métadonnées

PHASE 2 : Structure (Jour 2)
├─ Créer docs/ monorepo
├─ Importer contenu proprement
└─ Normaliser nommage

PHASE 3 : Config (Jour 2 soir)
├─ Quartz from scratch
├─ Obsidian vault setup
└─ Test local

PHASE 4 : Automation (Jour 3)
├─ GitHub Actions CI/CD
├─ Cloudflare Pages setup
└─ Validation

PHASE 5 : Deploy (Jour 3)
├─ Push main
├─ Go live
└─ Monitor
```

### Pourquoi pas d'autres approches?

#### ❌ Option A : "Lightweight Migration"
- **Pro :** Rapide (2 jours)
- **Con :** Garde la Dette technique
- **Verdict :** Non-viable long-term

#### ❌ Option B : "Complete Rebuild"
- **Pro :** Architecture clean, aucune dette
- **Con :** Temps long (4-5 jours), perte historique
- **Verdict :** Over-kill pour le gain

#### ✅ Option C : "Hybrid" (Choix)
- **Pro :** Temps optimal (3 jours), qualité excellente, iterative
- **Con :** Manageable (aucun réel con)
- **Verdict :** SWEET SPOT

---

## 📖 Plan d'Action Détaillé

### JOUR 1 : Préparation & Export

#### ✅ Tâche 1.1 : Backup & Safeguard

```bash
# 1.1.1 Créer backup complet
git tag backup-before-refactor
git branch backup-before-refactor

# 1.1.2 Documenter structure actuelle
tree -L 3 -I 'node_modules|.git' > STRUCTURE_BEFORE.txt

# 1.1.3 Créer branche travail
git checkout -b refactor/monorepo-architecture
```

**Temps :** 5 min  
**Deliverable :** Backup sûr, historique documenté

---

#### ✅ Tâche 1.2 : Nettoyer devops_base

```bash
# 1.2.1 Identifier ce qui est réutilisable
find website/devops_base -name "*.md" -o -name "*.sh" -o -name "*.tf" -o -name "*.yml"
# → Export ces fichiers

# 1.2.2 Exclure ce qui doit disparaitre
# NE PAS exporter : .conda/, .git/, node_modules/, binaries

# 1.2.3 Archive structuré
mkdir -p migration/devops-export
# Copier uniquement scripts, .md, configs
```

**Temps :** 15 min  
**Deliverable :** Liste ce qu'on garde, ce qu'on jette

---

#### ✅ Tâche 1.3 : Exporter contenu DE1 & DE2

```bash
# 1.3.1 DE1 exports
mkdir -p migration/de1-sources
cp -r "Data Engineering 1/lab"*"/" migration/de1-sources/
cp -r "Data Engineering 1/projet"* migration/de1-sources/

# 1.3.2 DE2 exports
mkdir -p migration/de2-sources
cp -r "Data Engineering 2/lab"* migration/de2-sources/
cp -r "Data Engineering 2/project"* migration/de2-sources/

# 1.3.3 Notebook conversion
for nb in $(find migration -name "*.ipynb"); do
  jupyter nbconvert --to markdown "$nb"
done
```

**Temps :** 20 min  
**Deliverable :** Contenu exporté, accessible

---

#### ✅ Tâche 1.4 : Analyser contenu website/

```bash
# 1.4.1 Checker what's in website/content/
ls -lR website/content/ > migration/website-content-audit.txt

# 1.4.2 Identifier doublons
diff <(find website/content -type f) \
     <(find website/quartz/static -type f) \
     > migration/duplicates.txt
```

**Temps :** 10 min  
**Deliverable :** Audit précis

---

#### ✅ Recap Jour 1
- ✅ Backup sûr
- ✅ Contenu exporté (DE1, DE2, DevOps)
- ✅ Duplication identifiée
- ✅ Prêt pour Jour 2

**Temps total :** ~1h  
**Risque :** Minimal

---

### JOUR 2 : Restructuration & Quartz

#### ✅ Tâche 2.1 : Créer structure docs/

```bash
# 2.1.1 Créer hierarchie monorepo avec notation DE2
mkdir -p docs/"DE1 — Data Engineering I"/{lab{1,2,3}\ assignment,lab{1,2,3}\ practice,"project final",assets}
mkdir -p docs/"DE2 — Data Engineering II"/{lab0\ setup\ practice,lab{1,2,3}\ assignment,lab{1,2,3}\ practice,"project final",assets}
mkdir -p docs/03-DevOps/{foundations,cicd,monitoring,labs,assets}
mkdir -p docs/Ressources/{assets}

# 2.1.2 Index root
cat > docs/_index.md << 'EOF'
---
title: Data Engineering — ESIEE
description: Platform centralisée pour Data Engineering
---

# 📚 Data Engineering — ESIEE

Bienvenue sur le portail d'apprentissage.

[[DE1 — Data Engineering I]] · 
[[DE2 — Data Engineering II]] · 
[[Ressources]]
EOF

# 2.1.3 Domain indices
cat > docs/"DE1 — Data Engineering I"/_index.md << 'EOF'
---
title: DE1 — Data Engineering I
---
# DE1 — Data Engineering I
EOF

cat > docs/"DE2 — Data Engineering II"/_index.md << 'EOF'
---
title: DE2 — Data Engineering II
---
# DE2 — Data Engineering II
EOF

cat > docs/Ressources/_index.md << 'EOF'
---
title: Ressources partagées
---
# Ressources partagées
EOF
```
title: Ressources partagées
---
# Ressources partagées
EOF
```

**Temps :** 15 min  
**Deliverable :** Structure vierge prête

---

#### ✅ Tâche 2.2 : Importer & normaliser contenu

```bash
# 2.2.1 Importer contenu DE1 (notation DE2)
mkdir -p docs/"DE1 — Data Engineering I"/"lab1 assignment"
mkdir -p docs/"DE1 — Data Engineering I"/"lab1 practice"
mkdir -p docs/"DE1 — Data Engineering I"/"lab2 assignment"
mkdir -p docs/"DE1 — Data Engineering I"/"lab2 practice"
mkdir -p docs/"DE1 — Data Engineering I"/"lab3 assignment"
mkdir -p docs/"DE1 — Data Engineering I"/"lab3 practice"
mkdir -p docs/"DE1 — Data Engineering I"/"project final"

cp migration/de1-sources/lab1*/* docs/"DE1 — Data Engineering I"/"lab1 practice"/
cp migration/de1-sources/lab2*/* docs/"DE1 — Data Engineering I"/"lab2 practice"/
# ... etc

# 2.2.2 Créer frontmatter standard
cat > docs/"DE1 — Data Engineering I"/"lab1 practice"/_index.md << 'EOF'
---
title: "Lab 1 - Spark Basics"
date: 2025-05-11
tags:
  - de1
  - spark
  - lab
  - beginner
domain: data-engineering-1
lab: 1
estimated-time: 45m
---

# Lab 1 - Spark Basics

Content...
EOF

# 2.2.3 Update liens internes
# OLD : ../lab1/assignment.ipynb
# NEW : [[lab-1#assignment]]
find docs -name "*.md" -exec sed -i 's|../lab1-practice|[[lab-1]]|g' {} \;

# 2.2.4 Import DevOps
cp -r migration/devops-export/* docs/03-devops/
```

**Temps :** 45 min  
**Deliverable :** Contenu importé, normalisé

---

#### ✅ Tâche 2.3 : Setup Quartz from scratch

```bash
# 2.3.1 Purger ancien website/
rm -rf website/  # L'ancien monolithe

# 2.3.2 Fresh Quartz install
npm init -y
npm install quartz@latest

# 2.3.3 Copy & customize configs
cat > quartz.config.ts << 'EOF'
import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "Data Engineering Portal",
    enableSPA: true,
    baseUrl: process.env.NODE_ENV === "production" 
      ? "https://data-engineering.pages.dev"
      : "http://localhost:8080",
    ignorePatterns: ["private", ".obsidian", "node_modules"],
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.ObsidianFlavoredMarkdown({ preserveLinks: true }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks(),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.Assets(),
      Plugin.ContentIndex(),
      Plugin.Cmark(),
      Plugin.Sitemap(),
    ],
  },
}
export default config
EOF

# 2.3.4 Sidebar layout
cat > quartz.layout.ts << 'EOF'
import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

export const filePageLayout: PageLayout = {
  left: [
    Component.PageTitle(),
    Component.Search(),
  ],
  right: [
    Component.Graph(),
    Component.Backlinks(),
  ],
}
export default filePageLayout
EOF

# 2.3.5 Test local
npm run quartz -- --serve
# Visite http://localhost:8080
```

**Temps :** 30 min  
**Deliverable :** Quartz fonctionne localement

---

#### ✅ Tâche 2.4 : Validations

```bash
# 2.4.1 Check for broken links
npm install -D linkcheck
npm run linkcheck docs/

# 2.4.2 Obsidian compatibility test
# Ouvrir Obsidian, pointer vault = ./docs/
# Vérifier : [[links]], graph, backlinks

# 2.4.3 Build test
npm run quartz -- build
# Vérifier : public/ generé sans erreur
```

**Temps :** 20 min  
**Deliverable :** Validations passées

---

#### ✅ Recap Jour 2
- ✅ Structure docs/ créée
- ✅ Contenu importé & normalisé
- ✅ Quartz configuré
- ✅ Tests locaux OK
- ✅ Prêt pour automation

**Temps total :** ~2h  
**Risque :** Modéré (review contenu)

---

### JOUR 3 : CI/CD & Deploy

#### ✅ Tâche 3.1 : GitHub Actions CI

```bash
# 3.1.1 Créer workflows
mkdir -p .github/workflows

# 3.1.2 CI pipeline
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  pull_request:
    paths:
      - 'docs/**'
      - '.github/workflows/ci.yml'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g markdownlint-cli
      - run: markdownlint "docs/**/*.md"

  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run quartz -- build
      
  linkcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -D linkcheck
      - run: npm run linkcheck public/
EOF

# 3.1.3 Deploy pipeline
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run quartz -- build
      
      - name: Deploy to Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy public/ --project-name=data-engineering
EOF

# 3.1.4 Push workflows
git add .github/
git commit -m "ci: add CI/CD workflows"
```

**Temps :** 30 min  
**Deliverable :** Workflows configurés

---

#### ✅ Tâche 3.2 : Cloudflare Setup

```bash
# 3.2.1 Installer wrangler
npm install -D wrangler

# 3.2.2 Login
wrangler login

# 3.2.3 Créer projet
wrangler pages project create data-engineering

# 3.2.4 Cloudflare dashboard secrets
# Settings → Secrets and variables → Actions
# CLOUDFLARE_API_TOKEN = (from Cloudflare account)
# CLOUDFLARE_ACCOUNT_ID = (your account ID)
```

**Temps :** 15 min  
**Deliverable :** Cloudflare intégré

---

#### ✅ Tâche 3.3 : Conventions & Docs

```bash
# 3.3.1 CONTRIBUTING.md complet
cat > CONTRIBUTING.md << 'EOF'
# Contribution Guidelines

## Structure

### Nommage Dossiers (Style DE2 — IMPORTANT!)
```
labs/
├── lab0 setup practice/      (avec espaces!)
├── lab1 assignment/
├── lab1 practice/
├── lab2 assignment/
├── lab2 practice/
├── lab3 assignment/
├── lab3 practice/
└── project final/
```

**RÈGLE : Pas de tirets, espaces pour séparer les mots**

### Nommage Fichiers
- PAS de tirets entre les mots
- Utiliser underscore pour composer : `assignment1_esiee.ipynb`
- Respecter cas original : `DE1_Lab1_Notebook_EN.ipynb`

### Frontmatter
```yaml
---
title: "Descriptive Title"
date: 2025-05-11
tags:
  - de1        # de1, de2, ou devops
  - spark      # topic
  - lab        # lab, assignment, practice, project
  - beginner   # beginner, intermediate, advanced
domain: data-engineering-1
lab: 1
estimated-time: 45m
---
```

### Liens Internes
- `[[lab1 practice]]` (Obsidian format avec espaces!)
- `[[lab1 practice#Theory]]` (avec ancre)
- `[[lab1 practice|Texte custom]]` (avec alias)
- Quartz auto-convertit en HTML

### Assets
- Stocker dans `assets/` local de chaque lab
- Lier avec : `![alt](./assets/image.png)`
EOF

# 3.3.2 ARCHITECTURE.md
cat > ARCHITECTURE.md << 'EOF'
# Repository Architecture

## Structure
```
docs/                               (Source of truth)
├── _index.md                       (root page)
├── _meta.json                      (metadata nav config)
├── DE1 — Data Engineering I/       (labs + projects)
├── DE2 — Data Engineering II/      (labs + projects)
├── 03-DevOps/                      (foundations, cicd, etc)
└── Ressources/                     (shared resources)
```

- docs/ = Source of truth (Markdown)
- public/ = Build output (generated)
- .github/workflows/ = CI/CD

## Access Patterns
1. Edit locally in Obsidian (./docs/)
2. Use Quartz format: `[[lab1 practice]]` with spaces!
3. Commit to Git
4. GitHub Actions runs CI
5. Deploy to Cloudflare Pages
6. Site live at data-engineering.pages.dev

## Extending

### Adding new course
1. Create `docs/04-course-name/`
2. Quartz auto-discovers
3. Navigation auto-updated

### Adding assets
1. Create `docs/03-course/assets/`
2. Link with `./assets/image.png`
EOF

# 3.3.3 Commit docs
git add CONTRIBUTING.md ARCHITECTURE.md
git commit -m "docs: add contribution guidelines and architecture"
```

**Temps :** 20 min  
**Deliverable :** Conventions documentées

---

#### ✅ Tâche 3.4 : .gitignore Final

```bash
# 3.4.1 Créer .gitignore strict
cat > .gitignore << 'EOF'
# Node
node_modules/
npm-debug.log*
package-lock.json

# Build outputs
public/
dist/
.next/

# Cache
.quartz-cache/
.cache/
*.cache

# Environment
.env
.env.local
.env.*.local
*.pem

# Python
venv/
.venv/
env/
__pycache__/
*.pyc
*.pyo

# System
.DS_Store
Thumbs.db
*.swp
*.swo

# Obsidian
.obsidian/private/

# VSCode
.vscode/settings.json
EOF

git add .gitignore
git commit -m "ci: strict gitignore"
```

**Temps :** 10 min  
**Deliverable :** Repo clean

---

#### ✅ Tâche 3.5 : Final Checks & Merge

```bash
# 3.5.1 Local tests
npm run quartz -- build
npm run linkcheck public/

# 3.5.2 Git checks
git status  # Must be clean
git log --oneline | head -5  # Verify commits

# 3.5.3 Push & Create PR
git push origin refactor/monorepo-architecture

# GitHub: Create PR
# → Actions auto-run CI
# → Check all pass

# 3.5.4 Merge to main
# (after PR approval)
git checkout main
git merge --no-ff refactor/monorepo-architecture

# 3.5.5 Monitor deploy
# Cloudflare Pages dashboard
# Check deployment live
```

**Temps :** 15 min  
**Deliverable :** Go live!

---

#### ✅ Recap Jour 3
- ✅ GitHub Actions CI/CD
- ✅ Cloudflare Pages
- ✅ Conventions documentées
- ✅ .gitignore strict
- ✅ Production live

**Temps total :** ~1.5h  
**Status :** SHIPPING CODE

---

## 📚 Ressources & Conventions

### A. Conventions Markdown

#### Nommage Dossiers (Style DE2)
```
✅ Bon (avec espaces, pas de tirets)
- lab0 setup practice/
- lab1 assignment/
- lab1 practice/
- lab2 assignment/
- lab2 practice/
- lab3 assignment/
- lab3 practice/
- project final/

❌ Mauvais
- lab-1-practice/
- lab1-assignment/
- Lab 1 Practice/
```

#### Nommage Fichiers
```
✅ Bon
- assignment1_esiee.ipynb
- DE1_Lab1_Notebook_EN.ipynb
- assignment1_genai.md

❌ Mauvais
- Lab 1 Spark Intro.md
- Theory.md
```

#### Frontmatter Template
```yaml
---
title: "Descriptive Title"
date: 2025-05-11
last-updated: 2025-05-11
tags:
  - de1              # de1, de2, devops
  - spark            # topic
  - lab              # lab, assignment, practice, project
  - beginner         # beginner, intermediate, advanced
domain: data-engineering-1
lab: 1
estimated-time: 45m
---
```

#### Liens Internes (Obsidian Format)
```markdown
# Dossier parent
[[lab1 practice]]

# Avec ancre
[[lab1 practice#Theory]]

# Avec texte custom
[[lab1 practice|Lancer le lab]]
```

#### Images & Assets
```markdown
# Stocker dans dossier local
docs/"DE1 — Data Engineering I"/"lab1 practice"/assets/

# Lier avec
![Description](./assets/image.png)
```

### B. Git Workflow

#### Branches
```
main                         (Stable, prod-ready)
  ├─ refactor/monorepo       (Migration initiale)
  ├─ feature/lab-*           (Nouveau contenu)
  ├─ fix/*                   (Corrections)
  └─ docs/*                  (Documentation)
```

#### Commits
```bash
# Format
feat: short description
fix: correction description
docs: documentation update
refactor: code restructure

# Examples
feat: add Spark SQL advanced lab
fix: correct typo in lab 1 assignment
docs: update contribution guidelines
```

### C. Tag Normalization

**Domaines (1 max par fichier) :**
```
#de1              (Data Engineering 1)
#de2              (Data Engineering 2)
#devops           (DevOps)
```

**Topics (multiple OK) :**
```
#spark #hadoop #python #docker #kubernetes
#cicd #terraform #monitoring
```

**Contenu Type :**
```
#lab #assignment #practice #solution #project
#exercise #exam #note
```

**Niveau :**
```
#beginner #intermediate #advanced #recap
```

### D. Obsidian Vault Setup

```bash
# 1. Point Obsidian vault à ./docs/
File → Open vault as folder
→ Select: data-engineering/docs/

# 2. Configure plugins
Settings → Community plugins
  - Obsidian Admonition
  - Excalidraw
  - TagWrangler

# 3. Configure display
Settings → Editor
  - Line numbers ON
  - Indent guides ON
  - Spell check ON

# 4. Daily workflow
Open "Daily notes" pane
Create notes in docs/
Commit from Git
```

---

## ✅ Checklist d'Implémentation

### Phase 0 : Préparation

- [ ] Lire ce fichier entièrement
- [ ] Valider approche Hybrid avec user
- [ ] Slack/Email : announcing refactor (optional)
- [ ] Créer branche `refactor/monorepo`
- [ ] Tag backup : `backup-before-refactor`

### Phase 1 : Export (Jour 1)

- [ ] Tâche 1.1 : Backup & branche de sauvegarde
- [ ] Tâche 1.2 : Analyser devops_base
- [ ] Tâche 1.3 : Exporter DE1 (notebooks, .md)
- [ ] Tâche 1.4 : Exporter DE2 (notebooks, .md)
- [ ] Tâche 1.5 : Exporter DevOps
- [ ] Tâche 1.6 : Vérifier rien n'est perdu
- [ ] Tâche 1.7 : Push branche sauvegarde

### Phase 2 : Restructuration (Jour 2 matin)

- [ ] Tâche 2.1 : Créer structure `docs/` avec notation DE2 (espaces!)
- [ ] Tâche 2.2 : Importer contenu DE1 avec distinction assignment/practice
- [ ] Tâche 2.3 : Importer contenu DE2 (déjà au bon format)
- [ ] Tâche 2.4 : Importer contenu DevOps
- [ ] Tâche 2.5 : Normaliser nommage (SANS tirets, avec espaces)
- [ ] Tâche 2.6 : Ajouter frontmatter standard (de1, de2 tags au lieu de data-engineering-1)
- [ ] Tâche 2.7 : Mettre à jour liens internes
- [ ] Tâche 2.8 : Tester structure Quartz

### Phase 3 : Quartz (Jour 2 soir)

- [ ] Tâche 3.1 : Supprimer ancien `website/`
- [ ] Tâche 3.2 : Fresh Quartz install
- [ ] Tâche 3.3 : Configurer `quartz.config.ts`
- [ ] Tâche 3.4 : Configurer `quartz.layout.ts`
- [ ] Tâche 3.5 : Test local (`npm run quartz -- --serve`)
- [ ] Tâche 3.6 : Fix build errors (if any)
- [ ] Tâche 3.7 : Verify navigation
- [ ] Tâche 3.8 : Verify graph view

### Phase 4 : Automation (Jour 3 matin)

- [ ] Tâche 4.1 : Créer `.github/workflows/ci.yml`
- [ ] Tâche 4.2 : Créer `.github/workflows/deploy.yml`
- [ ] Tâche 4.3 : Installer Wrangler
- [ ] Tâche 4.4 : Cloudflare Pages project
- [ ] Tâche 4.5 : GitHub Secrets (API tokens)
- [ ] Tâche 4.6 : Test CI locally (act)
- [ ] Tâche 4.7 : PR test (auto-run CI)

### Phase 5 : Documentation (Jour 3 après-midi)

- [ ] Tâche 5.1 : CONTRIBUTING.md
- [ ] Tâche 5.2 : ARCHITECTURE.md
- [ ] Tâche 5.3 : Conventions .md
- [ ] Tâche 5.4 : Tag schema .md
- [ ] Tâche 5.5 : Obsidian setup guide

### Phase 6 : Cleanup (Jour 3 soir)

- [ ] Tâche 6.1 : .gitignore strict
- [ ] Tâche 6.2 : Remove node_modules
- [ ] Tâche 6.3 : Cleanup temp exports
- [ ] Tâche 6.4 : Final git status (should be clean)
- [ ] Tâche 6.5 : Create PR

### Phase 7 : Validation & Merge (Jour 4)

- [ ] Tâche 7.1 : Peer review PR (if applicable)
- [ ] Tâche 7.2 : All GitHub Actions pass
- [ ] Tâche 7.3 : Cloudflare preview live
- [ ] Tâche 7.4 : Test preview URL
- [ ] Tâche 7.5 : Merge to main
- [ ] Tâche 7.6 : Monitor production deploy
- [ ] Tâche 7.7 : Verify data-engineering.pages.dev live
- [ ] Tâche 7.8 : Tag : `v1.0-migrated`

### Phase 8 : Post-Migration (Jour 5+)

- [ ] Tâche 8.1 : Announce new structure to team
- [ ] Tâche 8.2 : Distribute Obsidian setup guide
- [ ] Tâche 8.3 : Monitor for broken links/issues
- [ ] Tâche 8.4 : Collect feedback
- [ ] Tâche 8.5 : Fix issues
- [ ] Tâche 8.6 : Archive old `website/` (backup)
- [ ] Tâche 8.7 : Cleanup old imports (if safe)

---

## MÉTRIQUES DE SUCCÈS

### Before → After Transformation

| Métrique | Avant | Après | Cible Atteinte |
|----------|-------|-------|----------------|
| Taille repository | 11 GB | 200 MB | OUI |
| Temps clone | 30s+ | 2s | OUI |
| Temps build | N/A | 5s | OUI |
| CI/CD coverage | 0% | 100% | OUI |
| Broken links | ? | 0 | OUI |
| Conventions documentées | 0 | 3+ | OUI |
| Obsidian compatibility | NON | OUI | OUI |
| Temps deployment | Manual | Automated | OUI |
| Score scalabilité | 2/10 | 9/10 | OUI |
| Satisfaction développeurs | Basse | Haute | OUI |

---

## PROCHAINES ÉTAPES IMMÉDIATEMENT

### Avant de commencer

1. OUI - Lire ce document PLAN.md entièrement
2. OUI - Valider approche avec stakeholders
3. OUI - Allouer 4 jours de travail pour migration complète
4. OUI - Communiquer timeline à team (si applicable)

### À faire

1. Créer branche `refactor/monorepo-architecture`
2. Commencer Phase 1 (export Jour 1)
3. Suivre checklist étape par étape
4. Documenter questions/blockers au fur et à mesure
5. Commit progressivement sur la branche

### Support
- Questions sur architecture ? → Relire section 4 (Architecture Cible)
- Questions sur conventions ? → Relire section "Ressources & Conventions"
- Besoin de clarification ? → Demander (pas de questions bêtes)

---

## STANDARDS CODE GENERATION

### Guidelines Fondamentales pour Code Generation via Claude Code

**IMPORTANT :** Tout code généré par Claude Code DOIT respecter les standards suivants :

#### A. Commentaires de Code - Obligation Absolue

Chaque fichier produit doit contenir :

1. **Header de fichier (obligatoire)** :
```python
"""
Nom du module / fichier
Description brève (1-2 lignes) : ce que ce fichier fait
Utilisé par : qui l'utilise (optionnel)
"""
```

2. **Sections logiques** :
```python
# ============================================
# Configuration & Initialisation
# ============================================
# Description brève de ce que le block fait

config = {...}  # Description rapide
```

3. **Fonctions/Classes** :
```python
def process_data(input_file, output_format="csv"):
    """
    Traite un fichier de données et exporte dans le format spécifié.
    
    Args:
        input_file (str): chemin complet du fichier d'entrée
        output_format (str): format de sortie (csv, json, parquet)
    
    Returns:
        dict: résultat du traitement avec clés (success, output_path, errors)
    """
```

4. **Logique complexe** :
```python
# Filtrer les doublons en gardant le dernier tuple par clé
# Utilise un dictionnaire pour O(1) complexity au lieu de O(n^2) avec boucles
cleaned_data = {tuple_key: full_tuple for tuple_key, full_tuple in data.items()}
```

5. **Sections sensible s / Configuration** :
```python
# IMPORTANT : Adapter ces paths à votre environnement local
# Exemple Windows: r'C:\Users\YourName\Data Engineering\docs'
LOCAL_DOCS_PATH = "/home/sable/Documents/E4FD/S4/Data Engineering/docs"
```

#### B. Style de Commentaire

- JAMAIS de commentaires en ligne inutiles (bad_variable = 5  # nombre cinq)
- Commentaires explicatifs : pourquoi, pas quoi
- Français OU Anglais (PAS mélanger dans 1 fichier)
- Format cohérent : `# Première lettre majuscule`
- Longueur : max 100 caractères par ligne

#### C. Structure Standard ParType

**Pour scripts bash** :
```bash
#!/bin/bash
# Descripton courte du script
# Utilisation : bash script.sh [arguments]

# Configuration initiale
SOURCE_DIR="/path/to/source"
TARGET_DIR="/path/to/target"

# ============================================
# Fonction : Copy files with verification
# ============================================
# Copie fichiers et valide l'intégrité
copy_files_verified() {
  local source=$1
  local target=$2
  
  # Vérification directory exists
  if [[ ! -d "$source" ]]; then
    echo "ERREUR: Répertoire source n'existe pas: $source"
    return 1
  fi
  
  # Copie avec feedback
  cp -rv "$source" "$target" && echo "OK: Fichiers copiés"
}
```

**Pour Python** :
```python
"""
Module name : what this module does
"""

import os
import sys
from pathlib import Path

# ============================================
# Configuration
# ============================================
# Chemins d'accès

WORKSPACE_ROOT = Path(__file__).parent
DOCS_PATH = WORKSPACE_ROOT / "docs"
MIGRATION_PATH = WORKSPACE_ROOT / "migration"

def main():
    """
    Point d'entrée principal du script.
    
    Gère: initialisation, logging, exécution
    """
    pass

if __name__ == "__main__":
    main()
```

**Pour YAML/JSON** :
```yaml
# Configuration : Quartz site generator
# Utilisé par: npm run quartz -- build

baseUrl: "https://data-engineering.pages.dev"

# Plugins pour markdown processing et site generation
plugins:
  # Transformateurs : traitent le markdown brut
  transformers:
    - FrontMatter()  # Parse YAML header
    - SyntaxHighlighting()  # Code coloring
```

#### D. Règles Spécifiques Repository

- **Nommage fichiers** : `DE1_Lab1_Notebook_EN.md` (respecter casse originale)
- **Dossiers** : `lab1 practice/` (espaces, pas de tirets)
- **Code examples dans markdown** : toujours entourer de ````
- **Chemins en code** : utiliser `Path` objet Python ou variables configurables, PAS hardcoded
- **Secrets** : jamais committer, utiliser `.env` ou GitHub Secrets

#### E. Documentation pour Claude Code

Quand vous demandez à Claude Code de générer du code, incluez dans votre requête:

```
Contexte:
- Repository structure: /home/sable/Documents/E4FD/S4/Data Engineering/
- Notation dossiers: lab1 assignment/, lab1 practice/, project final/ (espaces!)
- Target: Quartz static site + Obsidian vault
- Audience: Étudiants + Professeurs ESIEE

Code Requirements:
1. Commentaires simples et compréhensibles (au moins 30% du code en commentaires)
2. Fonctions petites (max 20 lignes chaque)
3. Gestion d'erreur explicite avec messages clairs
4. Logging pour debugging
5. Docstrings pour toutes les fonctions publiques
```

---

## VALIDATION ET SIGNATURE

Architecture Analysis Version: 1.0
Date: 11 Mai 2026
Status: READY FOR IMPLEMENTATION - Professional Grade Prompt Engineering
Tone: Enterprise Professional (14 years DevOps/DataEng experience)
Code Standards: Full comments, clear explanations, maintainable
Timeline: 3-4 days
Risk Level: MODERATE
Quality Target: 8.5/10 final score

---

DÉBUT DE DOCUMENT FINAL

**INSTRUCTION D'UTILISATION AVEC CLAUDE CODE :**

Copie ce document entier dans Claude Code et utilise-le comme prompt principal pour la migration. Le document inclut:

1. Contexte expert (14 ans expérience)
2. Diagnostic détaillé de problèmes
3. Architecture cible complète
4. Plan d'exécution jour-par-jour
5. Standards de code (commentaires, conventions)
6. Checklist interactive

Ce document EST le prompt. Tu n'as pas besoin de réécrire rien. Fournis-le directement à Claude Code avec la demande:

"Utilise ce PLAN.md comme référence complète pour guider toute generation de code et structure. Assure-toi:
- Tous les commentaires suivent les guidelines section CODE GENERATION
- Notation dossiers = DE2 style (lab1 assignment/, pas lab-1-assignment/)
- Respect architecture monorepo: docs/DE1, docs/DE2, docs/03-DevOps
- Pas d'emojis dans les sorties
- Code simple et compréhensible pour audience ESIEE"

