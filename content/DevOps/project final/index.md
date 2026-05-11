---
date: 2026-05-11
description: 'Application EcoData Platform : backend, frontend, base de donnees, deploiement
  Docker + Kubernetes'
tags:
- devops
- ecodata-platform
title: Projet final DevOps - EcoData Platform
---

# Projet final DevOps - EcoData Platform

## L'application

EcoData Platform est l'application web livree comme projet final du cours DevOps.
L'architecture est compose de :

- **Backend** (`./ecodata-platform/backend/`) - service applicatif (Dockerfile fourni)
- **Frontend** (`./ecodata-platform/frontend/`) - interface utilisateur (Dockerfile fourni)
- **Base de donnees PostgreSQL** - declare comme `StatefulSet` Kubernetes
- **Orchestration locale** via `docker-compose.yml`
- **Deploiement cluster** via manifests dans `./ecodata-platform/k8s/`

[[ecodata-platform/index|>> Aller a EcoData Platform <<]]

## Documents racine

- [[DESIGN|DESIGN.md]] - decisions d'architecture
- [[README|README.md]] - documentation projet
- [[VISUAL_ASSETS|VISUAL_ASSETS.md]] - assets graphiques utilises

## Sous-arborescence

- [[ecodata-platform/index|ecodata-platform/]] - l'app complete
  - [[ecodata-platform/backend/index|backend/]] - Dockerfile + code serveur
  - [[ecodata-platform/frontend/index|frontend/]] - Dockerfile + code client
  - [[ecodata-platform/k8s/index|k8s/]] - 5 manifests Kubernetes
  - [[ecodata-platform/docs/index|docs/]] - design et assets visuels
  - [[ecodata-platform/uploads/index|uploads/]] - donnees d'entree
- [[proof/index|proof/]] - preuves de deploiement (a remplir)
