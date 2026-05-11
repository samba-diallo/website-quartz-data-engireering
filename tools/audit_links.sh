#!/usr/bin/env bash
# =============================================================
# audit_links.sh
# Verifie tous les wikilinks [[X]] / [[X|Y]] dans content/*.md
# par rapport au mode de resolution "relative" de Quartz :
# chaque target doit exister dans le meme dossier que la page
# qui le reference (ou sous forme de sous-dossier avec index.md).
# =============================================================

set +e

cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

broken_count=0
ok_count=0

# Extraire un wikilink par ligne en utilisant python pour robustesse
# (les fichiers contiennent des chemins avec espaces, accents, etc.)
extract_links() {
  local file="$1"
  python3 - "$file" << 'PY'
import re, sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
# Tous les wikilinks (Obsidian-style), capture la cible avant | ou ]
for m in re.finditer(r'\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]', text):
    target = m.group(1).strip()
    # Strip anchor portion
    if '#' in target:
        target = target.split('#', 1)[0]
    if target:
        print(target)
PY
}

# Pour chaque .md, pour chaque wikilink trouve, on resout vs dossier courant
while IFS= read -r -d '' f; do
  dir="$(dirname "$f")"

  while IFS= read -r target; do
    [[ -z "$target" ]] && continue
    resolved=""

    # Variantes : direct .md / file as-is / folder index
    if [[ -f "$dir/${target}.md" ]]; then
      resolved="$dir/${target}.md"
    elif [[ -f "$dir/${target}" ]]; then
      resolved="$dir/${target}"
    elif [[ -d "$dir/${target}" && -f "$dir/${target}/index.md" ]]; then
      resolved="$dir/${target}/index.md"
    elif [[ "$target" == */index ]]; then
      parent="${target%/index}"
      if [[ -f "$dir/${parent}/index.md" ]]; then
        resolved="$dir/${parent}/index.md"
      fi
    fi

    if [[ -z "$resolved" ]]; then
      printf "BROKEN  [[%s]]\n  in: %s\n" "$target" "$f"
      broken_count=$((broken_count+1))
    else
      ok_count=$((ok_count+1))
    fi
  done < <(extract_links "$f")
done < <(find content -name "*.md" -print0)

echo ""
echo "=============================================="
echo " Audit complete : $ok_count ok, $broken_count broken"
echo "=============================================="
