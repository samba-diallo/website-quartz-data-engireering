---
title: "Script de Déploiement Automatique - deploy-from-ghcr.sh"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Script de Déploiement Automatique

Le script `deploy-from-ghcr.sh` permet le déploiement automatisé complet de l'application EcoData Platform depuis GitHub Container Registry vers Minikube.

## Vue d'ensemble

Ce script bash automatise l'ensemble du processus de déploiement en :
- Vérifiant les prérequis système
- Démarrant Minikube si nécessaire
- Récupérant les images Docker depuis GHCR
- Déployant tous les composants Kubernetes
- Ouvrant l'application dans le navigateur

## Fonctionnalités

### Vérifications automatiques
- Présence de Minikube, kubectl et Docker
- État de Minikube (démarre automatiquement si nécessaire)
- Existence des manifests Kubernetes

### Gestion des images
- Pull automatique des images depuis GHCR
  - `ghcr.io/samba-diallo/devops/ecodata-backend:latest`
  - `ghcr.io/samba-diallo/devops/ecodata-frontend:latest`
- Chargement des images dans Minikube

### Déploiement Kubernetes
Le script applique les manifests dans l'ordre suivant :
1. **Namespace** : Création du namespace `ecodata`
2. **Secrets et PVC** : Configuration des credentials et volumes
3. **PostgreSQL** : Déploiement de la base de données
4. **Backend** : Déploiement de l'API FastAPI
5. **Frontend** : Déploiement de l'interface Streamlit

### Monitoring
- Attente que les pods soient prêts (60 secondes max)
- Affichage du statut complet du déploiement
- Ouverture automatique de l'application

## Utilisation

### Prérequis
```bash
# Vérifier les installations
minikube version
kubectl version --client
docker --version
```

### Exécution
```bash
# À la racine du projet
bash deploy-from-ghcr.sh
```

### Sortie attendue
```
========================================
  EcoData Platform - Déploiement GHCR  
========================================

[INFO] Vérification des prérequis...
[OK] Tous les prérequis sont satisfaits
[INFO] Vérification de Minikube...
[OK] Minikube est actif
[INFO] Pull des images depuis GHCR...
[INFO] Chargement des images dans Minikube...
[INFO] Déploiement sur Minikube...
[INFO] Attente que les pods soient prêts...
[OK] Pods prêts
[INFO] Ouverture de l'application...
[OK] Déploiement terminé avec succès!
```

## Structure du script

### Variables de configuration
```bash
NAMESPACE="ecodata"
BACKEND_IMAGE="ghcr.io/samba-diallo/devops/ecodata-backend:latest"
FRONTEND_IMAGE="ghcr.io/samba-diallo/devops/ecodata-frontend:latest"
K8S_DIR="projet-final-devops/ecodata-platform/k8s"
```

### Fonctions principales

#### `check_prerequisites()`
Vérifie la présence de tous les outils requis.

#### `check_minikube()`
Vérifie l'état de Minikube et le démarre si nécessaire.

#### `pull_images()`
Récupère les images Docker depuis GHCR.

#### `load_images_to_minikube()`
Charge les images dans le cluster Minikube.

#### `deploy_to_kubernetes()`
Applique tous les manifests Kubernetes dans l'ordre.

#### `wait_for_pods()`
Attend que tous les pods soient dans l'état `Ready`.

#### `show_status()`
Affiche l'état complet du déploiement (pods et services).

#### `open_application()`
Ouvre l'application dans le navigateur par défaut.

## Messages colorés

Le script utilise des couleurs pour améliorer la lisibilité :
- 🔵 **BLUE** : Informations générales
- 🟢 **GREEN** : Succès
- 🟡 **YELLOW** : Avertissements
- 🔴 **RED** : Erreurs

## Gestion des erreurs

Le script s'arrête immédiatement en cas d'erreur grâce à `set -e`.

### Erreurs courantes

**Minikube non installé :**
```
[ERROR] Minikube n'est pas installé. Veuillez l'installer d'abord.
```

**Répertoire k8s introuvable :**
```
[ERROR] Le répertoire projet-final-devops/ecodata-platform/k8s n'existe pas.
[ERROR] Assurez-vous d'être à la racine du repository Devops.
```

**Images GHCR inaccessibles :**
```
[WARNING] Impossible de pull l'image backend. Vérifiez vos permissions GHCR.
```

## Accès post-déploiement

### Commandes utiles
```bash
# Voir les pods
kubectl get pods -n ecodata

# Voir les services
kubectl get svc -n ecodata

# Accéder à l'application manuellement
minikube service ecodata-frontend -n ecodata

# Voir les logs
kubectl logs -n ecodata deployment/ecodata-backend -f
kubectl logs -n ecodata deployment/ecodata-frontend -f
```

## Téléchargement

Le script est disponible à la racine du projet :
- [Télécharger deploy-from-ghcr.sh](/static/devops/projet-final/deploy-from-ghcr.sh)

## Retour à la documentation

- [[devops/projet-final/ecodata-platform/index|Vue d'ensemble du projet]]
- [[devops/projet-final/ecodata-platform/documentation-projet-final-deploiement|Guide de déploiement complet]]
