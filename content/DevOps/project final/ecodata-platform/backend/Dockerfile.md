---
title: "Dockerfile"
date: 2026-05-11
tags:
  - devops
  - project
  - ecodata-platform
  - backend
draft: false
---

# Dockerfile

Fichier : `Dockerfile`  (477 octets, langage `dockerfile`)

[Telecharger le fichier brut](./Dockerfile)

## Contenu

```dockerfile
# Dockerfile pour le backend FastAPI
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer le dossier uploads
RUN mkdir -p uploads

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
