---
title: "TD1 - Introduction au Déploiement d'Applications"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# TD1 - Introduction au Déploiement d'Applications


## Aperçu

Le TD1 introduit les concepts fondamentaux du cloud computing et les bases du déploiement d'applications dans le cloud. Ce laboratoire se concentre sur la compréhension des différents modèles de déploiement et l'expérience pratique avec les services AWS.

## Objectifs

- Comprendre ce que sont les serveurs et comment ils fonctionnent
- Apprendre à déployer des applications localement
- Explorer les modèles de déploiement cloud (IaaS, PaaS, SaaS)
- Débuter avec AWS EC2 (Elastic Compute Cloud)
- Déployer une application Node.js simple dans le cloud

## Contenu du Lab

### 1. Déploiement Local

Le lab commence par l'exécution d'une simple application Node.js "Hello, World" en local :

- Création d'un serveur web minimal avec Node.js
- Compréhension du localhost et des interfaces réseau
- Test d'applications dans un environnement de développement local

### 2. Modèles de Cloud Computing

Introduction aux différents modèles de service :

- **IaaS (Infrastructure as a Service)**: AWS EC2 - Accès direct aux ressources de calcul
- **PaaS (Platform as a Service)**: AWS Elastic Beanstalk, Heroku - Plateforme gérée pour les applications
- **SaaS (Software as a Service)**: Applications entièrement gérées

### 3. Bases d'AWS EC2

Expérience pratique avec le service de calcul principal d'AWS :

- Compréhension des instances EC2 et des types d'instances
- Lancement et gestion de serveurs virtuels
- Connexion aux instances via SSH
- Groupes de sécurité de base et mise en réseau

### 4. Déploiement sur AWS

Déploiement pratique de l'application Node.js exemple :

- Préparation d'une application pour le déploiement cloud
- Configuration des instances EC2
- Exécution d'applications sur des serveurs distants
- Exposition des applications sur Internet

## Prérequis

- Compte AWS avec les identifiants appropriés
- Node.js installé localement (v23+ recommandé)
- Connaissances de base en ligne de commande
- Client SSH pour les connexions distantes

## Structure des Répertoires

```
td1/
├── README_TD1.md           # Ce fichier
├── lab1.pdf                # Instructions originales du lab
├── aws_support.txt         # Notes de configuration AWS
└── scripts/                # Scripts de déploiement et utilitaires
    ├── ec2-user-data-script/
    │   └── user-data.sh    # Script d'initialisation EC2
    └── sample-app/
        └── app.js          # Application Node.js exemple
```

## Concepts Clés Appris

1. **Développement Local**: Exécution d'applications sur votre propre machine avant le déploiement cloud
2. **Fondamentaux des Serveurs**: Comprendre ce qu'est un serveur et comment il diffère de localhost
3. **Services Cloud**: Différenciation entre les modèles IaaS, PaaS et SaaS
4. **AWS EC2**: Lancement et gestion de serveurs virtuels dans le cloud
5. **Déploiement Distant**: Passage du développement local à l'hébergement cloud prêt pour la production

## Fichiers Scripts

### Script User Data EC2
Le script d'initialisation automatique pour les instances EC2 est disponible :
- [user-data.sh](/static/devops/td1/scripts/user-data.sh)

### Application Node.js Exemple
L'application simple Node.js pour les tests :
- [app.js](/static/devops/td1/scripts/app.js)

## Démarrage

1. Consultez le document lab1.pdf pour des instructions détaillées
2. Configurez vos identifiants AWS
3. Suivez les exercices pour déployer l'application Node.js exemple
4. Expérimentez avec différents types d'instances EC2 et configurations

## Ressources

- Documentation AWS EC2: https://docs.aws.amazon.com/ec2/
- Site Officiel Node.js: https://nodejs.org/
- AWS Free Tier: https://aws.amazon.com/free/

## Notes

Ce TD établit les fondations pour les labs suivants qui s'appuient sur ces concepts de déploiement cloud, incluant l'Infrastructure as Code (TD2), les stratégies de déploiement avancées (TD3), et les pipelines CI/CD (TD5).
