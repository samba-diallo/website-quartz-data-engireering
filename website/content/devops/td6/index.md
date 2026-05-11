# TD6 - Multi-Environments et Multi-Services (NON RÉALISÉ)

**Auteurs**: DIALLO Samba, DIOP Mouhamed 
**Date**: 7 décembre 2025 
**Cours**: DevOps - ESIEE PARIS 
**Statut**: ABANDONNÉ pour raisons de coûts AWS

## Raison de l'abandon

Ce TD nécessite la création d'AWS Organizations et de multiples comptes AWS (dev, stage, prod), ce qui:
1. **Sort du AWS Free Tier** et active automatiquement un forfait payant
2. **Génère potentiellement des frais** même pour un usage académique
3. **N'est pas adapté** pour un projet étudiant avec compte gratuit

### Incident rencontré

Lors de la tentative de création des comptes AWS Organizations:
- Organisation créée: `o-f6p6stsx3q`
- Compte STAGE créé: `717892305920` (mouhamed.diop@edu.esiee.fr)
- Compte PROD créé: `097659826720` (production@esiee.fr)
- Compte DEV échoué: Email déjà utilisé
- **Mise à niveau automatique vers forfait payant**

### Actions correctives prises

1. **Destruction immédiate des comptes créés**
 ```bash
 cd td6/scripts/tofu/live/child-accounts
 tofu destroy -auto-approve
 ```
 - Comptes STAGE et PROD: Marqués pour suppression (90 jours)
 - Organisation: Reste active jusqu'à fermeture complète des comptes

2. **Vérification complète des ressources AWS**
 - Lambda functions: Aucune
 - EC2 instances: Aucune active
 - S3 buckets: Tous supprimés
 - DynamoDB tables: Toutes supprimées
 - API Gateway: Aucune

3. **Documentation créée**
 - `IMPORTANT_AWS_GRATUIT.md`: Guide de survie pour rester dans le Free Tier

## Objectifs du TD6 (non réalisés)

### Partie 1: Multi-Comptes AWS avec Organizations
**Objectif**: Isoler les environnements dev, stage, prod dans des comptes AWS séparés

**Pourquoi abandonné**: 
- Coûts potentiels
- Complexité de gestion
- Inadapté au Free Tier

### Partie 2: OpenTofu Workspaces
**Objectif**: Gérer plusieurs déploiements avec des workspaces

**Alternative gratuite possible**:
- Utiliser des workspaces dans un seul compte AWS
- Préfixer les ressources (dev-, stage-, prod-)
- Rester dans les limites du Free Tier

### Partie 3: Kubernetes Multi-Services
**Objectif**: Déployer frontend + backend dans Kubernetes

**Alternative 100% gratuite**:
- Docker Desktop avec Kubernetes activé (local)
- Minikube (local)
- Kind (local)
- Aucun coût AWS

## Structure existante

Fichiers préparés mais non utilisés:

```
td6/
├── README_TD6.md # Ce fichier
├── IMPORTANT_AWS_GRATUIT.md # Guide de sécurité AWS
├── lab6.pdf # Instructions originales
└── scripts/
 ├── sample-app-backend/ # Application backend Node.js
 │ ├── Dockerfile
 │ ├── app.js
 │ ├── server.js
 │ └── package.json
 ├── sample-app-frontend/ # Application frontend Node.js
 │ ├── Dockerfile
 │ ├── app.js
 │ ├── server.js
 │ └── package.json
 └── tofu/
 ├── live/
 │ ├── child-accounts/ # Création de comptes AWS (utilisé puis détruit)
 │ │ ├── main.tf
 │ │ └── outputs.tf
 │ ├── lambda-sample/ # Lambda pour workspaces
 │ └── lambda-sample-with-config/ # Lambda avec configuration
 └── modules/
 ├── aws-organizations/ # Module pour AWS Organizations
 └── test-endpoint/ # Module de test d'endpoints
```

## Leçons apprises

### Sur AWS Free Tier

1. **Services qui SORTENT du Free Tier**:
 - AWS Organizations
 - Création de comptes multiples
 - Services d'entreprise avancés

2. **Services qui RESTENT gratuits** (12 mois):
 - EC2: 750h/mois t2.micro ou t3.micro
 - Lambda: 1M requêtes/mois
 - S3: 5 GB de stockage
 - DynamoDB: 25 GB
 - API Gateway: 1M appels/mois

3. **Règle d'or**: 
 - Toujours détruire les ressources après les tests
 - Configurer des alertes de facturation
 - Vérifier quotidiennement les coûts

### Sur la gestion de projet DevOps

1. **Anticiper les coûts**: Vérifier les implications financières avant de déployer
2. **Documentation**: Toujours documenter les décisions et les abandons
3. **Alternatives locales**: Privilégier Docker/Kubernetes local pour l'apprentissage

## Alternatives recommandées pour l'apprentissage

### Pour apprendre les multi-environnements:

1. **Git Flow avec branches**
 - Branch `dev` pour développement
 - Branch `staging` pour tests
 - Branch `main` pour production

2. **Docker Compose avec profiles**
 ```yaml
 services:
 app:
 profiles: ["dev", "staging", "prod"]
 ```

3. **Variables d'environnement**
 - `.env.dev`
 - `.env.staging`
 - `.env.prod`

### Pour apprendre Kubernetes:

1. **Minikube** (recommandé pour débutants)
 ```bash
 minikube start
 kubectl apply -f deployments/
 ```

2. **Docker Desktop Kubernetes**
 - Activer dans Settings > Kubernetes
 - Utilisation simple et intégrée

3. **Kind (Kubernetes in Docker)**
 ```bash
 kind create cluster
 ```

## Coût final du projet

**Total dépensé**: $0.00 

Toutes les ressources ont été créées et détruites dans un délai très court:
- Comptes Organizations: ~10 minutes d'existence
- Aucune ressource AWS coûteuse active
- Nettoyage complet effectué

## Recommandations pour futurs TDs

1. **Toujours vérifier** si un TD nécessite des services payants
2. **Privilégier les alternatives locales** pour l'apprentissage
3. **Documenter les coûts** dans les énoncés de TP
4. **Prévoir des alternatives gratuites** pour les étudiants

## Conclusion

Le TD6 a été abandonné pour des raisons financières légitimes. Cependant, les compétences visées (multi-environnements, Kubernetes) peuvent être acquises via:
- Des alternatives locales (Docker, Kubernetes local)
- Une documentation théorique approfondie
- Des projets personnels avec technologies open-source

**Message important**: Il est préférable d'abandonner un TD que de générer des frais AWS imprévus. La décision est sage et responsable.

---

## Ressources utiles

- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Organizations Pricing](https://aws.amazon.com/organizations/pricing/)
- [Kubernetes local avec Minikube](https://minikube.sigs.k8s.io/docs/)
- [Docker Desktop Kubernetes](https://docs.docker.com/desktop/kubernetes/)
- [OpenTofu Workspaces](https://opentofu.org/docs/language/state/workspaces/)

## Support

Pour questions sur la gestion des coûts AWS:
- AWS Support: https://console.aws.amazon.com/support/home
- ESIEE IT Support: Contacter votre enseignant

---

## Fichiers Kubernetes

### Backend
- [sample-app-deployment.yml (backend)](/static/devops/td6/sample-app-deployment.yml)
- [sample-app-service.yml (backend)](/static/devops/td6/sample-app-service.yml)

### Frontend
- [sample-app-deployment.yml (frontend)](/static/devops/td6/sample-app-deployment.yml)
- [sample-app-service.yml (frontend)](/static/devops/td6/sample-app-service.yml)
