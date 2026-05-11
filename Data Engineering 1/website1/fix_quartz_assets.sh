#!/usr/bin/env bash

set -e

echo "🔧 Correction des assets Quartz (images et outputs)"

CONTENT_DIR="content"
STATIC_DIR="quartz/static"

LABS=("lab1" "lab2" "lab3")

IMG_EXTENSIONS=("png" "jpg" "jpeg" "svg")
TXT_EXTENSIONS=("txt" "md")

for LAB in "${LABS[@]}"; do
  echo "➡️  Traitement $LAB"

  mkdir -p "$STATIC_DIR/labs/$LAB/images"
  mkdir -p "$STATIC_DIR/labs/$LAB/outputs"

  if [ -d "$CONTENT_DIR/labs/$LAB" ]; then
    # Images
    for ext in "${IMG_EXTENSIONS[@]}"; do
      find "$CONTENT_DIR/labs/$LAB" -type f -name "*.${ext}" | while read -r file; do
        echo "   🖼️  Image déplacée : $file"
        mv "$file" "$STATIC_DIR/labs/$LAB/images/"
      done
    done

    # Text outputs
    for ext in "${TXT_EXTENSIONS[@]}"; do
      find "$CONTENT_DIR/labs/$LAB" -type f -name "*.${ext}" | while read -r file; do
        echo "   📄 Output déplacé : $file"
        mv "$file" "$STATIC_DIR/labs/$LAB/outputs/"
      done
    done
  fi
done

# Project assets
echo "➡️  Traitement projet final"
mkdir -p "$STATIC_DIR/project/images"
mkdir -p "$STATIC_DIR/project/outputs"

if [ -d "$CONTENT_DIR/project" ]; then
  for ext in "${IMG_EXTENSIONS[@]}"; do
    find "$CONTENT_DIR/project" -type f -name "*.${ext}" | while read -r file; do
      echo "   🖼️  Image déplacée : $file"
      mv "$file" "$STATIC_DIR/project/images/"
    done
  done

  for ext in "${TXT_EXTENSIONS[@]}"; do
    find "$CONTENT_DIR/project" -type f -name "*.${ext}" | while read -r file; do
      echo "   📄 Output déplacé : $file"
      mv "$file" "$STATIC_DIR/project/outputs/"
    done
  done
fi

echo "✅ Assets déplacés avec succès"
echo "ℹ️  Pense à corriger les liens Markdown vers /static/..."
