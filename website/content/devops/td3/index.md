---
title: "TD3 - Comment Déployer Vos Applications"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# TD3 - Comment Déployer Vos Applications

**Filière**: E4FD  
**Matière**: DevOps  
**Année académique**: 2025-2026  
**École**: ESIEE PARIS

## Documentation Complète

- [[devops/td3/readme|Documentation Complète du TD3 (Français)]]

## Description

Ce laboratoire explore 4 méthodes différentes de déploiement d'applications web sur AWS, du plus traditionnel (serveurs) au plus moderne (serverless).

## Objectif

Comprendre et comparer les différentes approches de déploiement d'applications :
- Orchestration de serveurs avec Ansible
- Orchestration de VMs avec Packer et OpenTofu
- Orchestration de conteneurs avec Docker et Kubernetes
- Architecture serverless avec AWS Lambda

## Structure du projet

```
td3/
├── scripts/
│   ├── ansible/          # Part 1: Ansible playbooks
│   ├── packer/           # Part 2: Packer templates
│   ├── tofu/             # Part 2 & 4: OpenTofu configurations
│   ├── docker/           # Part 3: Dockerfile et app
│   └── kubernetes/       # Part 3: Manifests Kubernetes
└── README_TD3.md         # Ce fichier
```

## Résumé global

TD3 "How to Deploy Your Apps" complété avec succès. Ce laboratoire a permis d'explorer et d'implémenter 4 méthodes différentes de déploiement d'applications.

### Statistiques globales

**Temps de réalisation**:
- Part 1: ~2 heures (avec troubleshooting)
- Part 2: ~2 heures (AMI build + déploiement)
- Part 3: ~1 heure (installation + déploiement)
- Part 4: ~30 minutes (configuration modules)
- **Total**: ~5.5 heures

**Ressources créées**:
- EC2 instances: 7 (4 Part 1, 3 Part 2)
- AMIs: 1 custom
- Load Balancers: 2 (1 Nginx, 1 ALB)
- Auto Scaling Groups: 1
- Lambda functions: 1
- API Gateways: 1
- IAM Roles: 1
- Docker images: 2
- Kubernetes pods: 3

## Part 1: Server Orchestration with Ansible

### Objectif
Déployer une application Node.js sur plusieurs serveurs EC2 en utilisant Ansible pour l'orchestration.

### Infrastructure déployée
- 3 instances EC2 t3.micro (serveurs d'application)
- 1 instance EC2 t3.micro (Nginx load balancer)
- Application Node.js 21.7.3 avec PM2 en mode cluster
- Nginx configuré comme reverse proxy

### Résultats
- Déploiement automatisé avec playbooks Ansible
- Inventaire dynamique AWS pour découverte automatique des instances
- Rolling updates implémentés avec changement de message
- Load balancing fonctionnel entre les 3 serveurs

### Status
Infrastructure terminée et détruite pour libérer les vCPUs (contrainte Free Tier AWS).

## Part 2: VM Orchestration with Packer and OpenTofu

### Objectif
Builder une image VM immutable avec Packer et la déployer avec OpenTofu.

### Infrastructure déployée
- AMI custom buildée avec Packer (ami-07804164695f58d34)
- Auto Scaling Group avec 3 instances t3.micro
- Application Load Balancer
- Health checks automatiques et auto-scaling configuré

### Résultats
- Image VM contenant Node.js, PM2 et l'application
- Infrastructure as Code avec OpenTofu
- Rolling update via instance refresh de l'ASG
- Application répond "OpenTofu Rocks!"

### Status
Infrastructure active et fonctionnelle.

### Endpoint
```
http://sample-app-alb-1026886045.us-east-2.elb.amazonaws.com
```

## Part 3: Container Orchestration with Docker and Kubernetes

### Objectif
Containeriser l'application avec Docker et la déployer sur un cluster Kubernetes local.

### Infrastructure déployée
- Docker 28.4.0 installé
- Cluster Kubernetes local avec Kind
- 3 pods répliqués de l'application
- Service Kubernetes pour l'accès interne

### Résultats
- Images Docker créées (v1 et v2)
- Déploiement Kubernetes avec 3 replicas
- Rolling update de v1 vers v2 réussi
- Configuration optimisée (maxSurge: 3, maxUnavailable: 0)
- Application répond "Kubernetes Rocks!"

### Status
Cluster local actif avec 3 pods fonctionnels.

## Part 4: Serverless with AWS Lambda

### Objectif
Déployer une fonction serverless avec AWS Lambda et API Gateway.

### Infrastructure déployée
- Fonction Lambda (Node.js 20.x, 128MB, 5s timeout)
- API Gateway HTTP API (route GET /)
- IAM Role avec permissions CloudWatch Logs
- Stage de déploiement automatique

### Résultats
- Fonction Lambda déployée avec OpenTofu en moins de 20 secondes
- API Gateway intégré avec la fonction Lambda
- Déploiement serverless sans gestion de serveur
- Application répond "Hello, World!"

### Status
Infrastructure active et fonctionnelle.

### Endpoint
```
https://2aveis6cl1.execute-api.us-east-2.amazonaws.com
```

## Prérequis

### Outils installés
- Ansible 2.16.3
- AWS CLI 2.31.24
- Packer 1.9.4
- OpenTofu 1.10.7
- Docker 28.4.0
- kubectl 1.34.2
- kind v0.20.0

### Configuration AWS
- Region: us-east-2
- Profile: labs-devops_diallo
- Account: 511211062907
- Instance type utilisé: t3.micro (Free Tier eligible)

## Comparaison des méthodes

| Méthode | Temps déploiement | Complexité | Maintenance | Scaling | Coût idle |
|---------|------------------|------------|-------------|---------|-----------|
| Ansible | 10-15 min | Moyenne | Haute | Manuel | Elevé |
| Packer/OpenTofu | 15-20 min | Moyenne | Moyenne | Automatique | Moyen |
| Docker/Kubernetes | 5 min | Elevée | Moyenne | Automatique | Faible |
| Lambda | < 1 min | Faible | Faible | Automatique | Nul |

## Utilisation recommandée

### Ansible
- Applications legacy nécessitant une configuration complexe
- Migrations progressives vers le cloud
- Environnements avec beaucoup de configuration manuelle

### Packer + OpenTofu
- Infrastructure immutable
- Besoins de conformité et d'audit
- Environnements reproductibles

### Docker + Kubernetes
- Applications microservices
- Besoin de portabilité multi-cloud
- Orchestration complexe de conteneurs

### AWS Lambda
- Applications event-driven
- Workloads intermittents
- API simples avec trafic variable

## Problèmes résolus

1. **Instance type**: Changement de t2.micro vers t3.micro (Free Tier us-east-2)
2. **vCPU limit**: Gestion de la limite de 16 vCPUs du Free Tier
3. **Docker permissions**: Utilisation de sudo pour les commandes Docker
4. **Kind images**: Chargement d'images locales avec pipe method
5. **OpenTofu modules**: Utilisation de modules locaux au lieu de remote GitHub

## Commandes de déploiement

### Part 1: Ansible
```bash
cd td3/scripts/ansible
export AWS_PROFILE=labs-devops_diallo
ansible-playbook create_ec2_instances_playbook.yml --extra-vars "@sample-app-vars.yml"
ansible-playbook -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
```

### Part 2: Packer + OpenTofu
```bash
cd td3/scripts/packer
packer build sample-app.pkr.hcl

cd ../tofu/live/asg-sample
tofu init
tofu apply
```

### Part 3: Docker + Kubernetes
```bash
cd td3/scripts/docker
docker build -t sample-app:v1 .

kind create cluster --name td3-cluster
docker save sample-app:v1 | kind load image-archive /dev/stdin --name td3-cluster

cd ../kubernetes
kubectl apply -f sample-app-deployment.yml
kubectl apply -f sample-app-service.yml
```

### Part 4: Lambda
```bash
cd td3/scripts/tofu/live/lambda-sample
export AWS_PROFILE=labs-devops_diallo
tofu init
tofu apply
```

## Tests

### Part 2: ALB
```bash
curl http://sample-app-alb-1026886045.us-east-2.elb.amazonaws.com
```

### Part 3: Kubernetes
```bash
kubectl get pods
kubectl exec -it <pod-name> -- curl localhost:8080
```

### Part 4: Lambda
```bash
curl https://2aveis6cl1.execute-api.us-east-2.amazonaws.com
```

## Nettoyage des ressources

### Détruire Part 2 (ASG + ALB)
```bash
cd td3/scripts/tofu/live/asg-sample
tofu destroy -auto-approve
```

### Détruire Part 4 (Lambda + API Gateway)
```bash
cd td3/scripts/tofu/live/lambda-sample
tofu destroy -auto-approve
```

### Nettoyer Part 3 (Kind cluster)
```bash
kind delete cluster --name td3-cluster
docker rmi sample-app:v1 sample-app:v2
```

## Leçons apprises

### Infrastructure as Code
- OpenTofu/Terraform: Reproductibilité et versioning
- Ansible: Idéal pour configuration management
- Modules réutilisables: Gain de temps majeur

### Containerisation
- Docker: Portabilité et isolation
- Kubernetes: Orchestration puissante mais complexe
- Kind: Excellent pour développement local

### Serverless
- Lambda: Scaling automatique et coût optimisé
- API Gateway: Intégration simple
- Limitation: Cold starts et timeouts

### AWS Constraints
- Free Tier: Limites vCPU (16 max)
- Instance types: t3.micro recommandé
- Régions: us-east-2 optimal pour labs

## Conclusion

TD3 complété avec succès. Nous avons exploré 4 paradigmes de déploiement:
1. **Traditional**: Ansible sur VMs
2. **Immutable Infrastructure**: Packer + OpenTofu
3. **Containers**: Docker + Kubernetes
4. **Serverless**: AWS Lambda

Chaque méthode a ses avantages selon le use case:
- **Ansible**: Legacy apps, configuration complexe
- **Packer/Tofu**: Immutable infrastructure, compliance
- **Docker/K8s**: Microservices, portabilité
- **Lambda**: Event-driven, coût optimisé

## Résultats obtenus

Les 4 parties du TD3 ont été complétées avec succès:
- Part 1: Ansible - TERMINE
- Part 2: Packer/OpenTofu - TERMINE
- Part 3: Docker/Kubernetes - TERMINE
- Part 4: AWS Lambda - TERMINE

Toutes les infrastructures sont fonctionnelles et testées.

## Ressources

- Livre: "Fundamentals of DevOps and Software Delivery" par Yevgeniy Brikman
- GitHub: https://github.com/brikis98/devops-book
- Labs AWS Academy: Account 511211062907

**Date de completion**: 6 décembre 2025
**Durée totale**: ~5.5 heures
**Status**: TOUS LES OBJECTIFS ATTEINTS

- Livre de référence: "Fundamentals of DevOps and Software Delivery" par Yevgeniy Brikman
- Repository GitHub: https://github.com/brikis98/devops-book
- AWS Academy Labs: Account 511211062907

## Auteur

Laboratoire réalisé dans le cadre de la formation DevOps.

Date de completion: 6 décembre 2024

---

## Fichiers Configuration

### Ansible
- [configure_nginx_playbook.yml](/static/devops/td3/configure_nginx_playbook.yml)
- [configure_sample_app_playbook.yml](/static/devops/td3/configure_sample_app_playbook.yml)
- [create_ec2_instances_playbook.yml](/static/devops/td3/create_ec2_instances_playbook.yml)
- [inventory.aws_ec2.yml](/static/devops/td3/inventory.aws_ec2.yml)

### Kubernetes
- [sample-app-deployment.yml](/static/devops/td3/sample-app-deployment.yml)
- [sample-app-service.yml](/static/devops/td3/sample-app-service.yml)
