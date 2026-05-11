#!/usr/bin/env bash
# =============================================================
# generate_proof_index.sh
# Pour chaque dossier proof/ sous content/, genere un index.md
# qui embarque :
#   - les screenshots (PNG/JPG) comme images
#   - les fichiers texte (.txt) en code blocks
#   - les autres fichiers (.json, .csv) comme liens telechargeables
#
# Usage : bash tools/generate_proof_index.sh [content/path/to/proof]
# Sans argument : traite TOUS les proof/ sous content/
# =============================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# -------- Determine list of folders to process ---------------
if [[ $# -ge 1 ]]; then
  TARGETS=("$1")
else
  mapfile -t TARGETS < <(find "${REPO_ROOT}/content" -type d -iname "proof" | sort)
fi

# -------- Helper : sanitize a string for title ---------------
guess_title() {
  # parent folder name -> readable title
  local parent
  parent="$(basename "$(dirname "$1")")"
  echo "${parent} - Preuves"
}

# -------- Helper : detect lab tag from path ------------------
guess_tags() {
  local p="$1"
  local tags="  - proof"
  [[ "$p" == *"Data Engineering 1"* ]] && tags+=$'\n  - de1'
  [[ "$p" == *"Data Engineering 2"* ]] && tags+=$'\n  - de2'
  [[ "$p" == *"assignment"* ]] && tags+=$'\n  - assignment'
  [[ "$p" == *"practice"* ]] && tags+=$'\n  - practice'
  [[ "$p" == *"project final"* ]] && tags+=$'\n  - project'
  echo "$tags"
}

# -------- Main loop ------------------------------------------
for proof_dir in "${TARGETS[@]}"; do
  if [[ ! -d "$proof_dir" ]]; then
    echo "SKIP (not a dir) : $proof_dir"
    continue
  fi

  title="$(guess_title "$proof_dir")"
  tags="$(guess_tags "$proof_dir")"
  index="${proof_dir}/index.md"

  # Open file with frontmatter
  {
    echo "---"
    echo "title: \"${title}\""
    echo "date: $(date +%Y-%m-%d)"
    echo "tags:"
    echo "${tags}"
    echo "draft: false"
    echo "---"
    echo ""
    echo "# ${title}"
    echo ""
    echo "Captures et plans d'execution generes lors du lab."
    echo ""
  } > "$index"

  # ---- Images section ----
  images=()
  while IFS= read -r -d '' f; do images+=("$f"); done < <(
    find "$proof_dir" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.svg" \) -print0 | sort -z
  )

  if [[ ${#images[@]} -gt 0 ]]; then
    {
      echo "## Captures d'ecran"
      echo ""
    } >> "$index"
    for img in "${images[@]}"; do
      bn="$(basename "$img")"
      # Alt = filename without extension
      alt="${bn%.*}"
      {
        echo "### ${alt}"
        echo ""
        echo "![${alt}](./${bn})"
        echo ""
      } >> "$index"
    done
  fi

  # ---- Text files section ----
  texts=()
  while IFS= read -r -d '' f; do texts+=("$f"); done < <(
    find "$proof_dir" -maxdepth 1 -type f -iname "*.txt" -print0 | sort -z
  )

  if [[ ${#texts[@]} -gt 0 ]]; then
    {
      echo "## Plans et logs"
      echo ""
    } >> "$index"
    for tx in "${texts[@]}"; do
      bn="$(basename "$tx")"
      {
        echo "### ${bn}"
        echo ""
        echo '```text'
        cat "$tx"
        echo ""
        echo '```'
        echo ""
      } >> "$index"
    done
  fi

  # ---- Other downloadable files (.json, .csv, .log) ----
  others=()
  while IFS= read -r -d '' f; do others+=("$f"); done < <(
    find "$proof_dir" -maxdepth 1 -type f \( -iname "*.json" -o -iname "*.csv" -o -iname "*.log" -o -iname "*.yml" -o -iname "*.yaml" \) -print0 | sort -z
  )

  if [[ ${#others[@]} -gt 0 ]]; then
    {
      echo "## Donnees brutes"
      echo ""
    } >> "$index"
    for o in "${others[@]}"; do
      bn="$(basename "$o")"
      ext="${bn##*.}"
      lang="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
      [[ "$lang" == "yml" ]] && lang="yaml"
      {
        echo "### ${bn}"
        echo ""
        echo "[Telecharger ${bn}](./${bn})"
        echo ""
        # Inline preview for small files
        if [[ $(stat -c%s "$o" 2>/dev/null || echo 999999) -lt 8000 ]]; then
          echo "\`\`\`${lang}"
          cat "$o"
          echo ""
          echo "\`\`\`"
          echo ""
        fi
      } >> "$index"
    done
  fi

  # ---- Subdirectories (e.g. DE1 lab3 has proof/screenshot/) ----
  subdirs=()
  while IFS= read -r -d '' d; do subdirs+=("$d"); done < <(
    find "$proof_dir" -maxdepth 1 -mindepth 1 -type d -print0 | sort -z
  )

  if [[ ${#subdirs[@]} -gt 0 ]]; then
    {
      echo "## Sous-dossiers"
      echo ""
    } >> "$index"
    for sd in "${subdirs[@]}"; do
      sd_name="$(basename "$sd")"
      # Count files inside
      n=$(find "$sd" -type f | wc -l)
      echo "- \`${sd_name}/\` (${n} fichiers)" >> "$index"
    done
    echo "" >> "$index"
  fi

  printf "[OK] %-80s (%d images, %d txt, %d data, %d dirs)\n" \
    "${proof_dir#${REPO_ROOT}/}" \
    "${#images[@]}" "${#texts[@]}" "${#others[@]}" "${#subdirs[@]}"
done
