---
title: "Frontend - Streamlit"
publish: true
---

# Frontend - Interface Streamlit

Interface web développée avec Streamlit pour permettre l'upload et la gestion des fichiers.

## Architecture

- **Framework**: Streamlit (Python)
- **Communication**: API REST avec le backend
- **Authentification**: Session-based

## Fichiers Sources

### Code Python

- [[devops/projet-final/frontend/app|app.py]] - Application Streamlit complète

### Configuration

- [Dockerfile](/static/devops/projet-final/frontend/Dockerfile)
- [requirements.txt](/static/devops/projet-final/frontend/requirements.txt)

## Fonctionnalités

### Page Publique
- Formulaire d'upload de fichiers (CSV/Excel)
- Champs: Nom, Email, Type de partenaire, Entreprise
- Upload multiple de fichiers

### Page Interne (Équipe)
- Authentification requise
- Liste de tous les fichiers uploadés
- Téléchargement des fichiers
- Suppression des fichiers
- Informations détaillées (nom, email, entreprise, date)

## Technologies

- Streamlit
- Pandas
- Requests (pour API calls)
- Python 3.10+
