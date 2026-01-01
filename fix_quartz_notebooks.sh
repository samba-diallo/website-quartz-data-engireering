
#!/usr/bin/env bash

set -e

echo "🔧 Correction de la structure Quartz (notebooks HTML)"

# Base directories
CONTENT_DIR="content"
STATIC_DIR="quartz/static"

# Labs list (adapter si besoin)
LABS=("lab1" "lab2" "lab3")

# Create static base folders
mkdir -p "$STATIC_DIR/labs"

for LAB in "${LABS[@]}"; do
  echo "➡️  Traitement $LAB"

  # Create target folder
  mkdir -p "$STATIC_DIR/labs/$LAB"

  # Move HTML notebooks from content to static
  if [ -d "$CONTENT_DIR/labs/$LAB" ]; then
    find "$CONTENT_DIR/labs/$LAB" -type f -name "*.html" | while read -r file; do
      echo "   📄 Déplacement : $file"
      mv "$file" "$STATIC_DIR/labs/$LAB/"
    done
  fi
done

# Project
echo "➡️  Traitement projet final"
mkdir -p "$STATIC_DIR/project"

if [ -d "$CONTENT_DIR/project" ]; then
  find "$CONTENT_DIR/project" -type f -name "*.html" | while read -r file; do
    echo "   📄 Déplacement : $file"
    mv "$file" "$STATIC_DIR/project/"
  done
fi

echo "✅ Déplacement terminé"
echo ""
echo "ℹ️  Rappels importants :"
echo "- Les fichiers HTML doivent être appelés via /static/..."
echo "- Aucun fichier HTML ne doit rester dans content/"
echo "- Vérifier la casse exacte des noms de fichiers"


