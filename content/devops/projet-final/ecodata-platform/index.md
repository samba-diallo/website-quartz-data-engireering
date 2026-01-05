---
title: "EcoData Platform"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# EcoData Platform

Plateforme complète de collecte et visualisation de données environnementales avec architecture cloud-native.

## Architecture

L'EcoData Platform est composée de plusieurs services orchestrés avec Kubernetes:

### Backend
API FastAPI pour la gestion des données environnementales.
- [[devops/projet-final/ecodata-platform/backend/index|Vue d'ensemble du Backend]]
- [[devops/projet-final/ecodata-platform/backend/main|Application FastAPI principale]]
- [[devops/projet-final/ecodata-platform/backend/database|Configuration de la base de données]]
- [[devops/projet-final/ecodata-platform/backend/models|Modèles SQLAlchemy]]
- [[devops/projet-final/ecodata-platform/backend/schemas|Schémas Pydantic]]

### Frontend
Interface Streamlit pour la visualisation des données.
- [[devops/projet-final/ecodata-platform/frontend/index|Vue d'ensemble du Frontend]]
- [[devops/projet-final/ecodata-platform/frontend/app|Application Streamlit]]

### Infrastructure Kubernetes
Manifestes pour le déploiement sur Kubernetes.
- Déploiements Backend et Frontend
- StatefulSet PostgreSQL
- Services et Ingress
- Configurations et Secrets

### Automatisation & CI/CD
Scripts et workflows pour l'automatisation complète du déploiement.
- [[devops/projet-final/ecodata-platform/ci-cd-pipeline|Pipeline CI/CD GitHub Actions]]
- [[devops/projet-final/ecodata-platform/deploy-from-ghcr|Script de déploiement automatique]]
- [Télécharger ci-cd-ghcr.yml](/static/devops/projet-final/ci-cd-ghcr.yml)
- [Télécharger deploy-from-ghcr.sh](/static/devops/projet-final/deploy-from-ghcr.sh)

### Documentation
- [[devops/projet-final/ecodata-platform/documentation-projet-final-deploiement|Guide de déploiement complet]]
- [[devops/projet-final/ecodata-platform/docs/DESIGN|Architecture et Design]]
- [[devops/projet-final/ecodata-platform/docs/VISUAL_ASSETS|Assets Visuels]]

## Fichiers Source

Tous les fichiers sources sont disponibles dans:
- [Backend Source](/static/devops/projet-final/backend/)
- [Frontend Source](/static/devops/projet-final/frontend/)
- [Manifestes Kubernetes](/static/devops/projet-final/k8s/)
- [Docker Compose](/static/devops/projet-final/docker-compose.yml)

## Technologies Utilisées

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Streamlit, Plotly
- **Infrastructure**: Kubernetes, Docker, GitHub Actions
- **Base de données**: PostgreSQL avec StatefulSet

## Déploiement

### Local avec Docker Compose
```bash
docker-compose up -d
```

### Production avec Kubernetes
```bash
kubectl apply -f k8s/
```

Voir la [[devops/projet-final/index|documentation complète du projet]] pour plus de détails.
