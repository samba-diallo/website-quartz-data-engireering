---
title: "Backend - FastAPI"
publish: true
---

# Backend - API FastAPI

Le backend est une API REST développée avec FastAPI pour gérer les uploads de fichiers et les utilisateurs.

## Architecture

- **Framework**: FastAPI (Python)
- **Base de données**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Fichiers Sources

### Code Python

- [[devops/projet-final/backend/main|main.py]] - Point d'entrée de l'API
- [[devops/projet-final/backend/database|database.py]] - Configuration DB
- [[devops/projet-final/backend/models|models.py]] - Modèles SQLAlchemy
- [[devops/projet-final/backend/schemas|schemas.py]] - Schémas Pydantic

### Configuration

- [Dockerfile](/static/devops/projet-final/backend/Dockerfile)
- [requirements.txt](/static/devops/projet-final/backend/requirements.txt)

## Endpoints API

- `POST /upload` - Upload de fichiers CSV/Excel
- `GET /files` - Liste des fichiers uploadés
- `GET /files/{file_id}/download` - Téléchargement d'un fichier
- `DELETE /files/{file_id}` - Suppression d'un fichier
- `POST /auth/register` - Création de compte
- `POST /auth/login` - Authentification

## Technologies

- FastAPI
- SQLAlchemy
- PostgreSQL
- Python 3.10+
