#!/bin/bash

# =============================================================================
# Script de déploiement automatique EcoData Platform depuis GHCR
# =============================================================================
# Ce script déploie automatiquement l'application EcoData Platform
# en utilisant les images Docker depuis GitHub Container Registry (GHCR)
#
# Prérequis:
# - Minikube installé et configuré
# - kubectl installé
# - Docker installé
# - Accès au repository GitHub samba-diallo/Devops
#
# Usage: bash deploy-from-ghcr.sh
# =============================================================================

set -e  # Arrêter en cas d'erreur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuration
NAMESPACE="ecodata"
BACKEND_IMAGE="ghcr.io/samba-diallo/devops/ecodata-backend:latest"
FRONTEND_IMAGE="ghcr.io/samba-diallo/devops/ecodata-frontend:latest"
K8S_DIR="projet-final-devops/ecodata-platform/k8s"

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Vérification des prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    if ! command_exists minikube; then
        log_error "Minikube n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    if ! command_exists kubectl; then
        log_error "kubectl n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    if ! command_exists docker; then
        log_error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    log_success "Tous les prérequis sont satisfaits"
}

# Vérifier et démarrer Minikube si nécessaire
check_minikube() {
    log_info "Vérification de Minikube..."
    
    if ! minikube status >/dev/null 2>&1; then
        log_warning "Minikube n'est pas démarré. Démarrage en cours..."
        minikube start --cpus=4 --memory=4096 --driver=docker
        log_success "Minikube démarré"
    else
        log_success "Minikube est actif"
    fi
}

# Pull des images depuis GHCR
pull_images() {
    log_info "Pull des images depuis GHCR..."
    
    log_info "Pull de l'image backend: $BACKEND_IMAGE"
    docker pull "$BACKEND_IMAGE" || {
        log_warning "Impossible de pull l'image backend. Vérifiez vos permissions GHCR."
    }
    
    log_info "Pull de l'image frontend: $FRONTEND_IMAGE"
    docker pull "$FRONTEND_IMAGE" || {
        log_warning "Impossible de pull l'image frontend. Vérifiez vos permissions GHCR."
    }
    
    log_success "Images récupérées depuis GHCR"
}

# Charger les images dans Minikube
load_images_to_minikube() {
    log_info "Chargement des images dans Minikube..."
    
    log_info "Chargement de l'image backend..."
    minikube image load "$BACKEND_IMAGE" 2>/dev/null || {
        log_warning "Image backend déjà présente dans Minikube"
    }
    
    log_info "Chargement de l'image frontend..."
    minikube image load "$FRONTEND_IMAGE" 2>/dev/null || {
        log_warning "Image frontend déjà présente dans Minikube"
    }
    
    log_success "Images chargées dans Minikube"
}

# Vérifier si le répertoire k8s existe
check_k8s_directory() {
    if [ ! -d "$K8S_DIR" ]; then
        log_error "Le répertoire $K8S_DIR n'existe pas."
        log_error "Assurez-vous d'être à la racine du repository Devops."
        exit 1
    fi
}

# Déployer l'application sur Kubernetes
deploy_to_kubernetes() {
    log_info "Déploiement sur Minikube..."
    
    # Créer le namespace
    log_info "Création du namespace $NAMESPACE..."
    kubectl apply -f "$K8S_DIR/namespace.yaml"
    
    # Créer les secrets et PVC
    log_info "Création des secrets et PVC..."
    kubectl apply -f "$K8S_DIR/secrets-and-pvc.yaml"
    
    # Déployer PostgreSQL
    log_info "Déploiement de PostgreSQL..."
    kubectl apply -f "$K8S_DIR/postgres-deployment.yaml"
    
    # Attendre que PostgreSQL soit prêt
    log_info "Attente que PostgreSQL soit prêt (30 secondes)..."
    sleep 30
    
    # Déployer le backend
    log_info "Déploiement du backend..."
    kubectl apply -f "$K8S_DIR/backend-deployment.yaml"
    
    # Déployer le frontend
    log_info "Déploiement du frontend..."
    kubectl apply -f "$K8S_DIR/frontend-deployment.yaml"
    
    log_success "Tous les manifests ont été appliqués"
}

# Attendre que les pods soient prêts
wait_for_pods() {
    log_info "Attente que les pods soient prêts (60 secondes max)..."
    
    kubectl wait --for=condition=ready pod \
        -l app=ecodata \
        -n "$NAMESPACE" \
        --timeout=60s 2>/dev/null || {
        log_warning "Certains pods prennent plus de temps que prévu"
        log_info "Vérifiez l'état avec: kubectl get pods -n $NAMESPACE"
    }
    
    log_success "Pods prêts"
}

# Afficher le statut du déploiement
show_status() {
    log_info "Statut du déploiement:"
    echo ""
    
    log_info "Pods:"
    kubectl get pods -n "$NAMESPACE"
    echo ""
    
    log_info "Services:"
    kubectl get svc -n "$NAMESPACE"
    echo ""
}

# Ouvrir l'application dans le navigateur
open_application() {
    log_info "Ouverture de l'application..."
    
    # Obtenir l'URL du service frontend
    minikube service ecodata-frontend -n "$NAMESPACE" &
    
    log_success "Application déployée avec succès!"
    echo ""
    log_info "Pour accéder manuellement à l'application, utilisez:"
    echo "  minikube service ecodata-frontend -n $NAMESPACE"
    echo ""
    log_info "Pour voir les logs:"
    echo "  Backend:  kubectl logs -n $NAMESPACE deployment/ecodata-backend -f"
    echo "  Frontend: kubectl logs -n $NAMESPACE deployment/ecodata-frontend -f"
}

# Fonction principale
main() {
    echo "========================================"
    echo "  EcoData Platform - Déploiement GHCR  "
    echo "========================================"
    echo ""
    
    check_prerequisites
    check_minikube
    check_k8s_directory
    pull_images
    load_images_to_minikube
    deploy_to_kubernetes
    wait_for_pods
    show_status
    open_application
    
    echo ""
    log_success "Déploiement terminé avec succès!"
}

# Exécuter le script
main
