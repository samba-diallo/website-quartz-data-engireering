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
#       docs/<rel-path>/<notebook>.md          (wrapper iframe)
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
#       "docs/DE1 - Data Engineering I/lab1 assignment"
#
# Si doc-target-dir n'est pas fourni, le script tente de deduire
# la cible en remplacant "Data Engineering N" par
# "docs/DEN - Data Engineering ..." et tirets par espaces.
# =============================================================

set -euo pipefail

# -------- Parametres -----------------------------------------
INPUT_NB="${1:-}"
TARGET_DIR="${2:-}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATIC_NB_ROOT="${REPO_ROOT}/static/nb"
DOCS_ROOT="${REPO_ROOT}/docs"

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

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERREUR : python3 introuvable"
  exit 1
fi

if ! python3 -c "import nbconvert, nbformat" 2>/dev/null; then
  echo "ERREUR : nbconvert/nbformat absents."
  echo "Installe : pip install nbformat nbconvert"
  exit 1
fi

# -------- Calcul des chemins de sortie -----------------------
NB_BASENAME="$(basename "${INPUT_NB}" .ipynb)"
NB_DIR="$(dirname "${INPUT_NB}")"

# Chemin relatif source par rapport au repo (pour structurer static/nb/)
REL_SOURCE="$(realpath --relative-to="${REPO_ROOT}" "${NB_DIR}")"
# Normalise pour URLs : remplace espaces par tirets, slashs preserves
SLUG_SOURCE="$(echo "${REL_SOURCE}" | sed 's/ /-/g; s|/-|/|g')"

STATIC_TARGET="${STATIC_NB_ROOT}/${SLUG_SOURCE}"
HTML_OUTPUT="${STATIC_TARGET}/${NB_BASENAME}.html"

# Determination du dossier wrapper .md
if [[ -n "${TARGET_DIR}" ]]; then
  WRAPPER_DIR="${REPO_ROOT}/${TARGET_DIR#./}"
else
  # Heuristique : "Data Engineering N/lab*-practice" -> docs/DE<N> .../lab* practice
  WRAPPER_DIR="${DOCS_ROOT}/${REL_SOURCE}"
fi

WRAPPER_MD="${WRAPPER_DIR}/${NB_BASENAME}.md"

# URL site-relative que l'iframe va charger
IFRAME_URL="/nb/${SLUG_SOURCE}/${NB_BASENAME}.html"

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
python3 -m nbconvert \
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
