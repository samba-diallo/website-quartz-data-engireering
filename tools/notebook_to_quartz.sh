#!/usr/bin/env bash
# =============================================================
# notebook_to_quartz.sh
# Convertit un Jupyter notebook en HTML rendu et l'integre dans
# le site Quartz via un wrapper Markdown contenant un <iframe>.
#
# Reproduit le contrat decrit par le prof Badr TAJINI dans la
# doc "node_support" (ESIEE Data Engineering, 2025-2026) :
#
#   - Input  : chemin absolu vers un .ipynb
#   - Output :
#       static/nb/<rel-path>/<notebook>.html   (rendu HTML)
#       content/<rel-path>/<notebook>.md       (wrapper iframe)
#
# Prerequisites :
#   - Python 3 + nbformat + nbconvert
#       (pip install nbformat nbconvert)
#   - Quartz config doit inclure Plugin.Assets() pour emettre
#     les fichiers non-MD presents dans static/.
#
# Usage :
#   bash tools/notebook_to_quartz.sh <notebook.ipynb> [doc-target-dir]
#
#   Exemples :
#     bash tools/notebook_to_quartz.sh \
#       "Data Engineering 1/lab1-practice/assignment1_esiee.ipynb"
#
#     bash tools/notebook_to_quartz.sh \
#       "Data Engineering 1/lab1-practice/assignment1_esiee.ipynb" \
#       "content/Data Engineering 1/lab1 assignment"
#
# Si doc-target-dir n'est pas fourni, le script ecrit le wrapper
# dans content/<chemin-relatif-source>/ (peut etre utile pour
# regenerer en place apres restructuration manuelle).
# =============================================================

set -euo pipefail

# -------- Parametres -----------------------------------------
INPUT_NB="${1:-}"
TARGET_DIR="${2:-}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Quartz Plugin.Static() copie quartz/static/* vers public/* au build,
# donc on ecrit le rendu HTML sous quartz/static/nb/ pour qu'il soit
# accessible a /nb/... cote site.
STATIC_NB_ROOT="${REPO_ROOT}/quartz/static/nb"
CONTENT_ROOT="${REPO_ROOT}/content"

# Python a utiliser pour nbconvert. Surcharge via :
#   PYTHON=de1-env/bin/python3 bash tools/notebook_to_quartz.sh ...
PYTHON="${PYTHON:-python3}"

# -------- Validations ----------------------------------------
if [[ -z "${INPUT_NB}" ]]; then
  echo "ERREUR : chemin du notebook manquant"
  echo "Usage : bash tools/notebook_to_quartz.sh <notebook.ipynb> [doc-target-dir]"
  exit 1
fi

if [[ ! -f "${INPUT_NB}" ]]; then
  echo "ERREUR : notebook introuvable : ${INPUT_NB}"
  exit 1
fi

if [[ "${INPUT_NB}" != *.ipynb ]]; then
  echo "ERREUR : extension attendue .ipynb, recu : ${INPUT_NB}"
  exit 1
fi

if ! command -v "${PYTHON}" >/dev/null 2>&1; then
  echo "ERREUR : python introuvable : ${PYTHON}"
  echo "Surcharge possible : PYTHON=/path/to/python3 bash $0 ..."
  exit 1
fi

if ! "${PYTHON}" -c "import nbconvert, nbformat" 2>/dev/null; then
  echo "ERREUR : nbconvert/nbformat absents dans ${PYTHON}"
  echo "Installe : ${PYTHON} -m pip install nbformat nbconvert"
  echo "Ou utilise une autre env via PYTHON=... (ex: PYTHON=de1-env/bin/python3)"
  exit 1
fi

# -------- Calcul des chemins de sortie -----------------------
NB_BASENAME="$(basename "${INPUT_NB}" .ipynb)"
NB_DIR="$(dirname "${INPUT_NB}")"

# Chemin relatif source par rapport au repo (pour structurer static/nb/)
REL_SOURCE="$(realpath --relative-to="${REPO_ROOT}" "${NB_DIR}")"

# Si le notebook est deja dans content/, on enleve le prefixe content/
# pour que l'URL soit propre (/nb/Data-Engineering-1/... au lieu de
# /nb/content/Data-Engineering-1/...)
REL_SOURCE_CLEAN="${REL_SOURCE#content/}"

# Normalise pour URLs : remplace espaces par tirets, slashs preserves
SLUG_SOURCE="$(echo "${REL_SOURCE_CLEAN}" | sed 's/ /-/g; s|/-|/|g')"

STATIC_TARGET="${STATIC_NB_ROOT}/${SLUG_SOURCE}"
HTML_OUTPUT="${STATIC_TARGET}/${NB_BASENAME}.html"

# Determination du dossier wrapper .md
if [[ -n "${TARGET_DIR}" ]]; then
  WRAPPER_DIR="${REPO_ROOT}/${TARGET_DIR#./}"
elif [[ "${REL_SOURCE}" == content/* ]]; then
  # Source deja dans content/ : on ecrit le wrapper a cote (in-place)
  WRAPPER_DIR="${REPO_ROOT}/${REL_SOURCE}"
else
  # Source hors content/ : on ecrit sous content/<chemin-relatif>/
  WRAPPER_DIR="${CONTENT_ROOT}/${REL_SOURCE}"
fi

WRAPPER_MD="${WRAPPER_DIR}/${NB_BASENAME}.md"

# URL site-relative que l'iframe va charger.
# Quartz Plugin.Static() copie quartz/static/* -> public/static/*,
# donc le prefixe URL est /static/.
IFRAME_URL="/static/nb/${SLUG_SOURCE}/${NB_BASENAME}.html"

# -------- Affichage du plan ----------------------------------
echo "============================================================"
echo "  notebook_to_quartz : conversion"
echo "============================================================"
echo "  Source notebook : ${INPUT_NB}"
echo "  Rendu HTML      : ${HTML_OUTPUT}"
echo "  Wrapper MD      : ${WRAPPER_MD}"
echo "  URL iframe      : ${IFRAME_URL}"
echo "============================================================"

mkdir -p "${STATIC_TARGET}" "${WRAPPER_DIR}"

# -------- Conversion nbconvert -------------------------------
# Format HTML "lab" (par defaut), sortie ecrasee a chaque appel
"${PYTHON}" -m nbconvert \
  --to html \
  --output-dir "${STATIC_TARGET}" \
  --output "${NB_BASENAME}.html" \
  "${INPUT_NB}"

# -------- Generation du wrapper Markdown ---------------------
# Frontmatter minimal + iframe responsive
cat > "${WRAPPER_MD}" <<EOF
---
title: "${NB_BASENAME}"
date: $(date +%Y-%m-%d)
tags:
  - notebook
draft: false
---

<iframe
  src="${IFRAME_URL}"
  width="100%"
  height="900"
  style="border:1px solid #ccc; border-radius:6px;"
  loading="lazy">
</iframe>

Source notebook : \`${REL_SOURCE}/${NB_BASENAME}.ipynb\`
EOF

echo ""
echo "[OK] Conversion terminee."
echo "     Tu peux maintenant lancer : npx quartz build"
