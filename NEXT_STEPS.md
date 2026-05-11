---
title: Next Steps - apres migration monorepo
date: 2026-05-11
---

# Prochaines etapes apres la migration

Le repository a ete restructure suivant `PLAN.md` + `PLAN_ADDENDUM_PROF.md`.
Etat actuel a la fin de la Phase 3 :

## Structure du repo

```
.
├── content/                          (Quartz source - SOURCE DE VERITE)
│   ├── index.md
│   ├── Data Engineering 1/
│   ├── Data Engineering 2/
│   ├── DevOps/
│   └── Ressources/
├── quartz/                           (Quartz framework v4.5.2)
├── tools/                            (Scripts automation)
│   ├── notebook_to_quartz.sh         (ipynb -> HTML + iframe wrapper)
│   └── generate_proof_index.sh       (proof/index.md auto-generation)
├── migration/                        (Archives Phase 1 - garder)
├── de1-env/                          (Python venv avec nbconvert)
├── Data Engineering 1/               (Sources originales - garder en reference)
├── Data Engineering 2/               (idem)
├── quartz.config.ts
├── quartz.layout.ts
├── package.json + tsconfig.json + package-lock.json
├── PLAN.md                           (plan initial)
├── PLAN_ADDENDUM_PROF.md             (adjustements suite consignes prof)
└── NEXT_STEPS.md                     (ce fichier)
```

## Git remote configure

- `origin` = https://github.com/samba-diallo/website-quartz-data-engireering.git
- Connexion verifiee via `git fetch origin` (succes)

**Pas encore pousse.** Les histoires locale et distante divergent (pas d'ancetre commun).

### Branches distantes detectees
- `origin/main`
- `origin/copilot/create-static-site-starter`
- `origin/dependabot/...`

### Branches locales
- `main` : commit cf5c83c (backup pre-refactor)
- `refactor/monorepo-architecture` : 7 commits structures (ou tu te trouves actuellement)

## Options pour pousser

### Option A - Force-push comme nouvelle main (le plus simple)

Remplace l'historique distant par notre arborescence propre.
Cloudflare redeploie automatiquement.

```bash
# Verifier que tu es bien sur refactor/monorepo-architecture
git status

# Renommer la branche locale en main
git branch -m refactor/monorepo-architecture main-new

# Push force vers origin/main
git push origin main-new:main --force
```

**Pour :** Histoire propre et structuree, deploiement immediat.
**Contre :** Tu perds l'historique GitHub existant (mais c'etait surtout des commits "y", "yes", "de1").

### Option B - Push comme nouvelle branche + PR

Conserve l'historique distant, te laisse review avant merge.

```bash
git push -u origin refactor/monorepo-architecture
```

Puis sur GitHub : crer une PR vers `main`. Tu pourras review chaque fichier
avant que le merge declenche le deploy Cloudflare.

**Pour :** Tracable, reviewable, reversible.
**Contre :** Necessite de gerer un conflit massif sur main au moment du merge
(strategy : "Squash and merge" ou "Replace main contents").

### Option C - Reset main local sur origin/main puis cherry-pick

Plus complexe, pas recommande sauf si tu tiens absolument a fusionner les
deux historiques.

## Une fois pousse - Cloudflare

Cloudflare Pages ecoute deja le push sur `main`. Verifier que :
1. Le build CF reussit (https://dash.cloudflare.com/pages)
2. Le site est live a https://website-quartz-data-engireering.pages.dev
3. Les notebooks iframes chargent bien (test local OK avec npx serve)
4. Les pages proof/ sont accessibles

## Contenu manquant (a recuperer ou ecrire)

### DE1 project final
Existant : Notebook + Report + un `Project.md` (1.7 KB).
Manquants suivant les consignes prof :
- Brief detaille
- Checklist d'evaluation
- Rubric / bareme

### DE2 project final
**Tout est manquant.** A recuperer aupres du prof :
- DE2_Project_Notebook_EN.ipynb
- DE2_Final_Project_Brief_EN
- DE2_Final_Project_Checklist_EN
- DE2_Final_Project_Rubric_EN
- DE2_Project_Report

Une fois recuperes, les placer dans `content/Data Engineering 2/project final/`
et lancer si necessaire `bash tools/notebook_to_quartz.sh <notebook>` pour le notebook.

### Support docs (DE1 et DE2)
Le screenshot du site prof montrait dans `support/` :
- `node_support.md` (Node, nvm, EBADENGINE)
- `oh-my-zsh_terminal_support.md`
- `README_OptionA.md`

Ces docs sont visibles sur le site du prof mais pas dans nos sources locales.
A recuperer.

## Commandes utiles

```bash
# Build local
npx quartz build

# Dev server avec hot reload
npx quartz build --serve

# Conversion d'un notebook (apres edit)
PYTHON=de1-env/bin/python3 bash tools/notebook_to_quartz.sh \
  "content/Data Engineering 1/lab1 practice/DE1_Lab1_Notebook_EN.ipynb"

# Regenerer toutes les proof/index.md (apres ajout de captures)
bash tools/generate_proof_index.sh

# Conversion en batch de TOUS les notebooks
find content -name "*.ipynb" | while read nb; do
  PYTHON=de1-env/bin/python3 bash tools/notebook_to_quartz.sh "$nb"
done
```

## Etat des phases

| Phase | Statut | Commit |
|---|---|---|
| 0 - Backup initial | OK | cf5c83c |
| 1 - Export + audit | OK | 7921796 |
| 1.5 - Strategie notebook prof | OK | 9c7d8c6 |
| 2 - Restructure content/ | OK | c9061cf |
| 2.5 - Quartz au root + verify build | OK | 12eb908 |
| 2.6 - proof/ pages | OK | e759dbf |
| 3 - Cleanup website/ + remote | OK | (ce commit) |
| 4 - Push GitHub | A faire | - |
| 5 - Verifier Cloudflare deploy | A faire | - |
| 6 - Recuperer contenu manquant | A faire | - |
