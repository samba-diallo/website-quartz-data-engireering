#!/usr/bin/env bash
# =============================================================
# generate_code_pages.sh
# Pour un dossier donne, scanne les fichiers code (Dockerfile,
# .yml, .yaml, .tf, .sh, .json, .csv, .conf, .toml) et :
#   1. Cree un wrapper .md par fichier code qui l'embarque
#      dans un fenced code block avec le bon langage
#   2. Cree un index.md du dossier listant tous les fichiers
#
# Usage :
#   bash tools/generate_code_pages.sh "content/DevOps/.../backend"
#   bash tools/generate_code_pages.sh "content/DevOps/.../k8s" "Manifests Kubernetes"
#
# Le fichier raw reste accessible (Plugin.Assets() le servira)
# mais une page MD lisible apparait dans la nav Quartz.
# =============================================================

set -euo pipefail

DIR="${1:-}"
TITLE_OVERRIDE="${2:-}"

if [[ -z "$DIR" || ! -d "$DIR" ]]; then
  echo "Usage : bash $0 <dossier> [titre]"
  exit 1
fi

# Determine title
if [[ -n "$TITLE_OVERRIDE" ]]; then
  TITLE="$TITLE_OVERRIDE"
else
  TITLE="$(basename "$DIR")"
fi

# Tag from path
TAGS="  - devops"
[[ "$DIR" == *"project final"* ]] && TAGS+=$'\n  - project'
[[ "$DIR" == *"ecodata"* ]] && TAGS+=$'\n  - ecodata-platform'
[[ "$DIR" == *"backend"* ]] && TAGS+=$'\n  - backend'
[[ "$DIR" == *"frontend"* ]] && TAGS+=$'\n  - frontend'
[[ "$DIR" == *"k8s"* ]] && TAGS+=$'\n  - kubernetes'
[[ "$DIR" == *"docker"* ]] && TAGS+=$'\n  - docker'

# Map extension -> code-block language
ext_to_lang() {
  case "$1" in
    yml|yaml) echo "yaml" ;;
    tf|tfvars) echo "hcl" ;;
    sh) echo "bash" ;;
    json) echo "json" ;;
    csv) echo "csv" ;;
    toml) echo "toml" ;;
    conf) echo "ini" ;;
    py) echo "python" ;;
    ts) echo "typescript" ;;
    js) echo "javascript" ;;
    Dockerfile|dockerfile) echo "dockerfile" ;;
    *) echo "text" ;;
  esac
}

# -------- Wrap each code file as a .md page ------------------
wrapped=0
declare -a wrappers=()
declare -a others=()

# Iterate non-recursively (just files at top level of $DIR)
shopt -s nullglob
for f in "$DIR"/*; do
  bn="$(basename "$f")"
  # Skip directories and existing .md
  [[ -d "$f" ]] && continue
  [[ "$bn" == "index.md" ]] && continue
  [[ "$bn" == *.md ]] && continue

  ext="${bn##*.}"
  # Dockerfile has no extension : use filename
  if [[ "$bn" == "Dockerfile" || "$bn" == Dockerfile.* ]]; then
    ext="Dockerfile"
  fi
  lang="$(ext_to_lang "$ext")"

  # Wrapper name : <basename>.md (collision if file name == .md already, but we skipped those)
  wrapper="$DIR/${bn}.md"

  # Inline only if reasonably small (<200 KB)
  size=$(stat -c%s "$f" 2>/dev/null || echo 0)
  {
    echo "---"
    echo "title: \"${bn}\""
    echo "date: $(date +%Y-%m-%d)"
    echo "tags:"
    echo "$TAGS"
    echo "draft: false"
    echo "---"
    echo ""
    echo "# ${bn}"
    echo ""
    echo "Fichier : \`${bn}\`  (${size} octets, langage \`${lang}\`)"
    echo ""
    echo "[Telecharger le fichier brut](./${bn})"
    echo ""
    if [[ "$size" -lt 204800 ]]; then
      echo "## Contenu"
      echo ""
      echo "\`\`\`${lang}"
      cat "$f"
      # Ensure trailing newline before closing fence
      [[ "$(tail -c1 "$f" | xxd -p)" != "0a" ]] && echo ""
      echo "\`\`\`"
    else
      echo "*Fichier trop gros pour preview inline (${size} octets). Utilise le lien telecharger.*"
    fi
  } > "$wrapper"

  wrappers+=("$bn")
  wrapped=$((wrapped+1))
done
shopt -u nullglob

# -------- Generate index.md ---------------------------------
index="$DIR/index.md"
{
  echo "---"
  echo "title: \"${TITLE}\""
  echo "date: $(date +%Y-%m-%d)"
  echo "tags:"
  echo "$TAGS"
  echo "---"
  echo ""
  echo "# ${TITLE}"
  echo ""
} > "$index"

# List subdirectories
shopt -s nullglob
subdirs=()
for d in "$DIR"/*/; do
  subdirs+=("$(basename "$d")")
done
shopt -u nullglob

if [[ "${#subdirs[@]}" -gt 0 ]]; then
  {
    echo "## Sous-dossiers"
    echo ""
    for sd in "${subdirs[@]}"; do
      echo "- [[${sd}/index|${sd}/]]"
    done
    echo ""
  } >> "$index"
fi

# List wrappers
if [[ "${#wrappers[@]}" -gt 0 ]]; then
  {
    echo "## Fichiers"
    echo ""
    for w in "${wrappers[@]}"; do
      echo "- [[${w}|${w}]]"
    done
    echo ""
  } >> "$index"
fi

# List .md files already in this folder (excluding index.md and the wrappers we just made)
shopt -s nullglob
existing_md=()
for f in "$DIR"/*.md; do
  bn="$(basename "$f")"
  [[ "$bn" == "index.md" ]] && continue
  # Skip wrappers we just created (they're called <code>.md)
  is_wrapper=0
  if [[ "${#wrappers[@]}" -gt 0 ]]; then
    for w in "${wrappers[@]}"; do
      if [[ "$bn" == "${w}.md" ]]; then is_wrapper=1; break; fi
    done
  fi
  [[ $is_wrapper -eq 1 ]] && continue
  existing_md+=("$bn")
done
shopt -u nullglob

if [[ "${#existing_md[@]}" -gt 0 ]]; then
  {
    echo "## Documents Markdown"
    echo ""
    for m in "${existing_md[@]}"; do
      slug="${m%.md}"
      echo "- [[${slug}|${m}]]"
    done
    echo ""
  } >> "$index"
fi

printf "[OK] %-70s : %d wrappers, %d subdirs, %d existing md\n" \
  "${DIR}" "$wrapped" "${#subdirs[@]}" "${#existing_md[@]}"
