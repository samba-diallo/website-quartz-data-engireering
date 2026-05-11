---
date: 2026-05-11
draft: false
tags:
- devops
- ecodata-platform
- frontend
title: Dockerfile
---

# Dockerfile

Fichier : `Dockerfile`  (464 octets, langage `dockerfile`)

[Telecharger le fichier brut](./Dockerfile)

## Contenu

```dockerfile
# Dockerfile pour le frontend Streamlit
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port 8501
EXPOSE 8501

# Commande pour lancer l'application Streamlit
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```
