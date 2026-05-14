# Mettre à jour le site — du notebook jusqu'à GitHub

Guide complet : que faire **à chaque fois que tu modifies quelque chose** pour que
le changement apparaisse sur le site déployé.

> Racine du projet (à adapter si besoin) :
> `/home/sable/Documents/E4FD/S4/Data Engineering`
> Toutes les commandes se lancent **depuis cette racine**, sauf indication contraire.

---

## 1. Comprendre l'architecture (à lire une fois)

Le site **n'affiche pas** les notebooks directement. Il y a 4 emplacements distincts :

| Emplacement | Rôle | On édite ? |
|---|---|---|
| `Data Engineering 2/<lab>/` | **La source** : notebooks `.ipynb`, `proof/`, notes `.md`… | ✅ **OUI, toujours ici** |
| `quartz/static/nb/Data-Engineering-2/<lab-slug>/` | **HTML rendu** affiché dans l'iframe de la page | ❌ généré — ne jamais éditer à la main |
| `content/Data Engineering 2/<lab>/` | **Miroir Quartz** : pages `.md`, copies `.ipynb` téléchargeables, `proof/` | ❌ généré/synchronisé — ne jamais éditer à la main |
| `public/` | Build final du site (ce que Cloudflare publie) | ❌ généré — ignoré par git |

**Flux complet :**

```
   Tu édites              Tu régénères              git push           Cloudflare
┌─────────────────┐   ┌──────────────────────┐   ┌──────────────┐   ┌─────────────┐
│ Data Engineering│──▶│ quartz/static/nb/... │──▶│ GitHub Actions│──▶│ Pages       │
│ 2/<lab>/  (.ipynb│   │ + content/...        │   │ npm run build │   │ (site live) │
│  proof/ ...)    │   │  (HTML + copies)     │   │   → public/   │   │             │
└─────────────────┘   └──────────────────────┘   └──────────────┘   └─────────────┘
     étape 1                  étape 2                  étape 3            auto
```

⚠️ **Éditer la source ne suffit pas.** Sans l'étape 2, le site continue d'afficher
l'ancienne version.

---

## 2. Tableau des chemins par lab

`<lab>` = nom avec espaces (dossiers réels) · `<lab-slug>` = nom avec tirets (URLs / `static/nb`)

| Lab | `<lab>` | `<lab-slug>` | Notebook |
|---|---|---|---|
| Lab 0 practice | `lab0 setup practice` | `lab0-setup-practice` | `DE2_Lab0_Starter.ipynb` |
| Lab 1 assignment | `lab1 assignment` | `lab1-assignment` | `assignment1_esiee.ipynb` |
| Lab 1 practice | `lab1 practice` | `lab1-practice` | `DE2_Lab1_Notebook_EN.ipynb` |
| Lab 2 assignment | `lab2 assignment` | `lab2-assignment` | `assignment2_esiee.ipynb` |
| Lab 2 practice | `lab2 practice` | `lab2-practice` | `DE2_Lab2_Notebook_EN.ipynb` |
| Lab 3 assignment | `lab3 assignment` | `lab3-assignment` | `assignment3_esiee.ipynb` |
| Lab 3 practice | `lab3 practice` | `lab3-practice` | `DE2_Lab3_Notebook_EN.ipynb` |

---

## 3. CAS A — J'ai modifié un notebook `.ipynb`

Tu édites **toujours** la source : `Data Engineering 2/<lab>/<notebook>.ipynb`
(c'est celui qui s'ouvre dans l'IDE). Ensuite, deux sous-cas.

### A.1 — J'ai modifié seulement du texte / markdown

(titre, noms, piste, commentaires… le code n'a pas changé OU je ne veux pas
de nouvelles sorties)

```bash
cd "/home/sable/Documents/E4FD/S4/Data Engineering"

# 1. Régénérer le HTML rendu (ce que l'iframe affiche)
de1-env/bin/python3 -m nbconvert --to html \
  --output-dir "quartz/static/nb/Data-Engineering-2/<lab-slug>" \
  --output "<notebook>.html" \
  "Data Engineering 2/<lab>/<notebook>.ipynb"

# 2. Recopier le .ipynb téléchargeable dans content/
cp "Data Engineering 2/<lab>/<notebook>.ipynb" \
   "content/Data Engineering 2/<lab>/<notebook>.ipynb"
```

**Exemple concret — lab2 assignment :**

```bash
cd "/home/sable/Documents/E4FD/S4/Data Engineering"

de1-env/bin/python3 -m nbconvert --to html \
  --output-dir "quartz/static/nb/Data-Engineering-2/lab2-assignment" \
  --output "assignment2_esiee.html" \
  "Data Engineering 2/lab2 assignment/assignment2_esiee.ipynb"

cp "Data Engineering 2/lab2 assignment/assignment2_esiee.ipynb" \
   "content/Data Engineering 2/lab2 assignment/assignment2_esiee.ipynb"
```

### A.2 — J'ai modifié du code ET je veux les nouvelles sorties

(nouveaux tableaux, prints, résultats Spark…)

Il faut **ré-exécuter** le notebook **avant** de régénérer le HTML, sinon le site
affiche le nouveau code mais les anciens résultats.

```bash
# 0. Ré-exécuter le notebook (depuis le dossier du lab, pour que les
#    chemins relatifs comme ../../sample_archive_github.json fonctionnent)
cd "/home/sable/Documents/E4FD/S4/Data Engineering/Data Engineering 2/<lab>"
"/home/sable/Documents/E4FD/S4/Data Engineering/de1-env/bin/python3" \
  -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  "<notebook>.ipynb"

# Puis revenir à la racine et faire les étapes 1 et 2 du cas A.1
cd "/home/sable/Documents/E4FD/S4/Data Engineering"
# ... (nbconvert --to html ...)  +  (cp ... content/ ...)
```

⚠️ La ré-exécution régénère aussi ce que le notebook écrit sur disque
(`outputs/`, `proof/plan_*.txt`, `*_metrics_log.csv`…). Pense à resynchroniser
le `proof/` si besoin (voir **CAS B**).

---

## 4. CAS B — J'ai modifié les preuves (`proof/` : captures, plans, logs)

Les captures d'écran et fichiers `plan_*.txt` vivent dans
`Data Engineering 2/<lab>/proof/`. La page `proof/index.md` du site est
**générée automatiquement** à partir des fichiers présents.

```bash
cd "/home/sable/Documents/E4FD/S4/Data Engineering"

# 1. Synchroniser les fichiers proof/ vers content/ (copie + supprime les obsolètes,
#    garde index.md)
rsync -a --delete --exclude='index.md' \
  "Data Engineering 2/<lab>/proof/" \
  "content/Data Engineering 2/<lab>/proof/"

# 2. Régénérer la page index.md du dossier proof/
bash tools/generate_proof_index.sh "content/Data Engineering 2/<lab>/proof"
```

---

## 5. CAS C — J'ai modifié une page Markdown (`index.md`, `ENGINEERING_NOTE.md`, `GENAI.md`…)

Deux situations :

- **Le fichier est déjà dans `content/`** (ex. un `index.md` de lab) →
  édite-le directement dans `content/Data Engineering 2/<lab>/`, rien d'autre à faire.
- **Le fichier vit dans la source** (`Data Engineering 2/<lab>/ENGINEERING_NOTE.md`…) →
  copie-le vers `content/` :
  ```bash
  cp "Data Engineering 2/<lab>/ENGINEERING_NOTE.md" \
     "content/Data Engineering 2/<lab>/ENGINEERING_NOTE.md"
  ```

> Les `*_metrics_log.csv` se copient de la même façon : `cp` source → `content/`.

---

## 6. Prévisualiser en local AVANT de pousser

```bash
cd "/home/sable/Documents/E4FD/S4/Data Engineering"
npx quartz build --serve
```

Ouvrir **http://localhost:8080** et vérifier la/les page(s) modifiée(s).
`Ctrl+C` pour arrêter. Port occupé ? → `npx quartz build --serve --port 8081`.

Vérifier au minimum :
- la page du notebook (l'iframe charge bien la **nouvelle** version) ;
- la page `proof/` si tu as touché aux preuves ;
- les liens du `index.md` du lab.

(Optionnel) build « comme en production », sans serveur :
```bash
NODE_ENV=production npm run build
```

---

## 7. Pousser sur GitHub → déploiement automatique Cloudflare

Le dépôt : `https://github.com/samba-diallo/website-quartz-data-engireering`
Branche de production : **`main`**.

```bash
cd "/home/sable/Documents/E4FD/S4/Data Engineering"

# 1. Voir ce qui a changé
git status

# 2. Ajouter les changements
#    (inclut content/, quartz/static/nb/, et la source Data Engineering 2/)
git add "Data Engineering 2" "content" "quartz/static/nb"
#    — ou tout d'un coup : git add -A

# 3. Commit avec un message clair
git commit -m "update(de2-lab2): corrige assignment2 + maj rendu"

# 4. Pousser
git push origin main
```

### Ce que le `push` déclenche automatiquement

Le push sur `main` lance **2 workflows GitHub Actions** (dossier `.github/workflows/`) :

1. **`ci.yml` — Build and Validate** : `npm ci` + `npm run build`, vérifie que
   `public/` est généré correctement.
2. **`deploy.yml` — Deploy to Cloudflare Pages** : rebuild puis déploie `public/`
   sur Cloudflare Pages (projet `website-quartz-data-engireering`).

Tu n'as **rien à configurer** : les secrets Cloudflare sont déjà en place.

### Vérifier le déploiement

- **GitHub Actions** : https://github.com/samba-diallo/website-quartz-data-engireering/actions
  → les 2 jobs doivent être verts ✅ (compter ~1–3 min).
- **Site en ligne** : https://website-quartz-data-engireering.pages.dev
  → recharge en vidant le cache (`Ctrl+Shift+R`) si tu vois encore l'ancienne version.

---

## 8. Checklist avant chaque push

- [ ] J'ai édité la **source** (`Data Engineering 2/...`), pas le miroir `content/`.
- [ ] J'ai régénéré le **HTML rendu** (`nbconvert --to html`) si j'ai touché un notebook.
- [ ] J'ai **ré-exécuté** le notebook si j'ai changé du code et veux les nouvelles sorties.
- [ ] J'ai recopié le `.ipynb` (et les `.md`/`.csv` source) dans `content/`.
- [ ] J'ai resynchronisé `proof/` + régénéré son `index.md` si j'ai touché aux preuves.
- [ ] `npx quartz build --serve` : la page modifiée s'affiche correctement en local.
- [ ] `git status` ne montre que des changements **attendus**.
- [ ] Message de commit clair, puis `git push origin main`.
- [ ] Workflows GitHub Actions verts ✅.

---

## 9. Dépannage rapide

| Symptôme | Cause probable | Solution |
|---|---|---|
| Mes modifs n'apparaissent pas sur le site | HTML rendu pas régénéré (étape 2 sautée) | Refaire **CAS A** |
| Le site montre le nouveau code mais d'anciens résultats | Notebook pas ré-exécuté | Refaire **CAS A.2** |
| Une capture d'écran est cassée (image absente) | `proof/` désynchronisé | Refaire **CAS B** |
| `nbconvert: command not found` / `No module named nbconvert` | nbconvert n'est que dans `de1-env` | Utiliser `de1-env/bin/python3 -m nbconvert ...` |
| La ré-exécution échoue sur le chemin du dataset | Lancée depuis le mauvais dossier | Lancer depuis `Data Engineering 2/<lab>/` (voir **CAS A.2**) |
| `git push` rejeté | Le remote a avancé | `git pull --rebase origin main` puis `git push` |
| Workflow GitHub Actions rouge ❌ | Erreur de build | Ouvrir le log dans l'onglet *Actions*, corriger, re-push |
| Site live pas à jour alors qu'Actions est vert | Cache navigateur / CDN | `Ctrl+Shift+R`, attendre 1–2 min |

---

## 10. Notes utiles

- **Ne jamais committer `public/`** ni `node_modules/` ni `de1-env/` → déjà dans `.gitignore`.
- Les fichiers `.html` sous `quartz/static/nb/`, eux, **doivent** être committés
  (c'est ce que l'iframe charge en production).
- `tools/notebook_to_quartz.sh` existe mais régénère aussi le wrapper `.md`
  (avec un chemin d'iframe à reprendre) — préférer les commandes manuelles de ce guide.
- L'audit `bash tools/audit_links.sh` signale de faux « BROKEN » sur les liens de
  tableau à pipe échappé (`[[.../index\|...]]`) dans les `index.md` — **les ignorer**.
