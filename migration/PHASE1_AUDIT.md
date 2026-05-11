---
title: Phase 1 Audit Report
date: 2026-05-11
phase: 1
status: completed
---

# Rapport d'audit - Phase 1 (Export & Préparation)

## Résumé exécutif

Phase 1 du plan de migration vers monorepo (cf. `PLAN.md`) exécutée avec succès.
Toutes les opérations sont **non destructives** : aucun fichier supprimé.

| Action | Statut | Résultat |
|---|---|---|
| Backup git | Fait | commit `cf5c83c` sur `main`, branche `refactor/monorepo-architecture` créée |
| .gitignore strict | Fait | 26 MB indexés (au lieu de 11 GB) |
| Export devops_base | Fait | `migration/devops-export/devops_base_source_files.tar.gz` (1.9 MB, 866 fichiers) |
| Export DE1 | Fait | `migration/de1-sources/de1_sources.tar.gz` (9.2 MB, 66 fichiers) |
| Export DE2 | Fait | `migration/de2-sources/de2_sources.tar.gz` (12 MB, 38 fichiers) |
| Export website | Fait | `migration/website-export/website_content.tar.gz` (3.9 MB, 186 fichiers) + configs Quartz |
| Structure documentée | Fait | `migration/STRUCTURE_BEFORE.txt` (302 lignes) |

**Total exporté : ~27 MB** (réutilisable pour la Phase 2 et au-delà).

---

## Écarts entre PLAN.md et réalité observée

Plusieurs hypothèses du plan se sont révélées inexactes ou incomplètes :

### 1. Le workspace n'était PAS un dépôt git
**Plan :** Toutes les tâches 1.1 et 3.5 utilisent `git tag`, `git checkout -b`, `git commit`.
**Réalité :** Aucun `.git/` à la racine. `git init -b main` exécuté en début de Phase 1.

### 2. Tailles sous-estimées dans le plan
| Composant | Plan annonce | Mesure réelle |
|---|---|---|
| `Data Engineering 1/` | ~50 MB | **2.7 GB** |
| └─ `website1/` | non quantifié | 1.2 GB (446 MB `node_modules`, 17 MB `public`, etc.) |
| └─ `projet-final/outputs/` | non mentionné | **1.1 GB** de sorties Spark |
| `Data Engineering 1/node_modules/` | non mentionné | 446 MB |
| `de1-env/` (Python venv) | non mentionné | 931 MB |

### 3. Dépôts git imbriqués non signalés
Deux `.git/` imbriqués détectés :
- `website/.git/` → renommé en `website/.git.archive/` (préservé)
- `Data Engineering 1/website1/.git/` → renommé en `.git.archive/` (préservé)

Sans ces renommages, le `git add` parent les ajoutait comme submodules cassés.

### 4. Dossiers non listés dans le plan
- `website/docs/` (2.4 MB, 76 .md + 15 .png) - tree de docs séparé
- `website/proof/` (2.2 MB, screenshots/preuves)
- `.claude/`, `.sixth/` - configs IDE/outils

---

## Inventaire des exports

### `migration/devops-export/devops_base_source_files.tar.gz` (1.9 MB)
866 fichiers source extraits de `website/devops_base/` (sur 9.4 GB total) :

| Type | Nombre |
|---|---|
| `.tf` (Terraform) | 380 |
| `.md` (docs) | 194 |
| `.yml` / `.yaml` | 98 |
| `.json` (configs) | 84 |
| `.sh` (scripts) | 66 |
| `.tfvars` | 12 |
| `Dockerfile` | 27 |
| `.csv` | 2 |

**Top-level :** `td0..td6/`, `projet-final-devops/`, scripts racine (`create-k8s-manifests.sh`, `IMPORTANT_AWS_GRATUIT.md`, `README.md`).

### `migration/de1-sources/de1_sources.tar.gz` (9.2 MB)
66 fichiers, contenu pédagogique DE1 :
- `lab1-practice/`, `lab2-practice/`, `lab3-practice/`, `projet-final/`
- Notebooks `.ipynb`, rapports `.md`, scripts Python, figures PNG
- **Exclus :** `outputs/` (1.1 GB Spark), `spark-warehouse/`, `.ipynb_checkpoints/`
- Note : `Data Engineering 1/lab1-practice/assets/` contient des duplicatas exacts des fichiers parents (à dédupliquer en Phase 2)

### `migration/de2-sources/de2_sources.tar.gz` (12 MB)
38 fichiers, contenu pédagogique DE2 :
- `lab0 setup practice/`, `lab1 assignment/`, `lab1 practice/`, `lab2 assignment/`, `lab2 practice/`, `lab3 assignment/`, `lab3 practice/`, `project final/`
- 7 notebooks `.ipynb`, 4 PDF, 2 .md, screenshots, configs
- **Confirme :** DE2 utilise déjà la nomenclature "espaces" cible

### `migration/website-export/` (3.9 MB tarball + configs)
- `website_content.tar.gz` : 186 fichiers de `website/content/`, `website/docs/`, `website/proof/`
- `quartz.config.ts`, `quartz.layout.ts`, `package.json` (à étudier pour Phase 3)

---

## Découvertes additionnelles

### Duplication website/ vs website1/
Confirmation du problème P5 du plan. Différences observées :
- `website/content/` est plus complet (contient `devops/`, `Project.md`, `Labs - Data Engineering.md`)
- `website1/` n'a PAS le sous-dossier `devops/`
- Les fichiers communs **divergent** (`index.md`, `lab2/index.md`, etc.)

**Recommandation Phase 2 :** abandonner `website1/`, prendre `website/` comme source.

### Incohérence nommage DE1 vs DE2 (confirmé)
| DE1 (tirets) | DE2 (espaces, format cible) |
|---|---|
| `lab1-practice/` | `lab1 practice/` |
| `lab2-practice/` | `lab2 practice/` |
| `lab3-practice/` | `lab3 practice/` |
| `projet-final/` (FR) | `project final/` (EN) |
| (pas de lab0) | `lab0 setup practice/` |
| (pas d'assignment séparé) | `lab1 assignment/`, `lab2 assignment/`, `lab3 assignment/` |

DE1 n'a **aucun** dossier "assignment" séparé : les `assignment*_esiee.ipynb` cohabitent dans `lab*-practice/`. Phase 2 devra créer les `lab* assignment/` DE1 à partir de ces fichiers.

---

## État git actuel

```
Branche actuelle : refactor/monorepo-architecture
Commits :
  cf5c83c chore: initial backup before monorepo refactor
```

`main` reste sur `cf5c83c` comme point de rollback complet.

---

## Prochaines étapes (Phase 2)

À valider avec l'utilisateur avant exécution :

1. **Créer `docs/` monorepo** avec sous-dossiers `DE1 — Data Engineering I/`, `DE2 — Data Engineering II/`, `03-DevOps/`, `Ressources/`
2. **Importer** depuis les tarballs `migration/*` en normalisant la nomenclature DE1 vers le style DE2 (espaces)
3. **Convertir** les notebooks `.ipynb` en Markdown via `jupyter nbconvert`
4. **Ajouter frontmatter** YAML standard à chaque page
5. **Supprimer** `website/` (et `website/devops_base/`, `website1/`) une fois la nouvelle structure validée

**Opérations destructives prévues - confirmation utilisateur requise avant Phase 2.**
