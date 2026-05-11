# TD5 - Preuves de Réalisation

**Auteurs**: DIALLO Samba, DIOP Mouhamed  
**Date**: 7 décembre 2025  
**Cours**: DevOps - ESIEE PARIS

## Vue d'ensemble

Ce document présente les preuves de la réalisation complète du TD5 sur l'intégration et le déploiement continus (CI/CD) avec GitHub Actions et AWS.

---

## Partie 1: CI (Continuous Integration)

### 1.1 Workflow de Tests d'Application (app-tests.yml)

**Fichier créé**: `.github/workflows/app-tests.yml`

**Preuve de création**:
- Workflow configuré pour tester l'application Node.js avec Jest
- Déclenché automatiquement sur chaque push et pull request
- Tests unitaires de l'application sample-app

**Résultat attendu**: Tous les tests passent avec succès

```yaml
name: Test Sample App
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd td5/scripts/sample-app && npm ci
      - run: cd td5/scripts/sample-app && npm test
```

---

### 1.2 Configuration AWS OIDC

**Infrastructure créée**:

#### S3 Bucket pour le State OpenTofu
- **Nom**: `samba-diallo-devops-tofu-state-2025`
- **Région**: us-east-2
- **Versioning**: Activé
- **Encryption**: AES256

**Commande de vérification**:
```bash
aws s3 ls s3://samba-diallo-devops-tofu-state-2025
```

#### DynamoDB Table pour le State Locking
- **Nom**: `samba-diallo-devops-tofu-state-2025`
- **Partition Key**: LockID (String)
- **Région**: us-east-2

**Commande de vérification**:
```bash
aws dynamodb describe-table --table-name samba-diallo-devops-tofu-state-2025 --region us-east-2
```

#### OIDC Provider GitHub
- **Provider URL**: `https://token.actions.githubusercontent.com`
- **Audience**: `sts.amazonaws.com`
- **Thumbprint**: Configuré pour GitHub Actions

**Commande de vérification**:
```bash
aws iam list-open-id-connect-providers
```

#### IAM Roles Créés

1. **lambda-sample-tests**
   - ARN: `arn:aws:iam::511211062907:role/lambda-sample-tests`
   - Permission: Exécuter `tofu test`
   - Trust Policy: GitHub Actions OIDC

2. **lambda-sample-plan**
   - ARN: `arn:aws:iam::511211062907:role/lambda-sample-plan`
   - Permission: Exécuter `tofu plan`
   - Trust Policy: GitHub Actions OIDC

3. **lambda-sample-apply**
   - ARN: `arn:aws:iam::511211062907:role/lambda-sample-apply`
   - Permission: Exécuter `tofu apply`
   - Trust Policy: GitHub Actions OIDC

**Commande de vérification**:
```bash
aws iam list-roles | grep lambda-sample
```

---

### 1.3 Workflow de Tests d'Infrastructure (infra-tests.yml)

**Fichier créé**: `.github/workflows/infra-tests.yml`

**Fonctionnalités**:
- Authentification AWS via OIDC (pas de credentials statiques)
- Installation d'OpenTofu
- Exécution de `tofu test` sur l'infrastructure Lambda
- Validation des endpoints API Gateway

**Preuve de sécurité**: Utilisation de OIDC au lieu de clés AWS statiques
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::511211062907:role/lambda-sample-tests
    aws-region: us-east-2
```

---

## Partie 2: CD (Continuous Deployment)

### 2.1 Workflow tofu-plan.yml

**Fichier créé**: `.github/workflows/tofu-plan.yml`

**Déclenchement**: Sur chaque Pull Request vers main

**Fonctionnalités**:
- Exécute `tofu plan` pour montrer les changements prévus
- Poste le plan en commentaire sur la PR
- Permet la revue des changements avant merge

**Configuration du backend S3**:
```hcl
terraform {
  backend "s3" {
    bucket         = "samba-diallo-devops-tofu-state-2025"
    key            = "td5/lambda-sample/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "samba-diallo-devops-tofu-state-2025"
    encrypt        = true
  }
}
```

---

### 2.2 Workflow tofu-apply.yml

**Fichier créé**: `.github/workflows/tofu-apply.yml`

**Déclenchement**: Après merge d'une PR vers main

**Fonctionnalités**:
- Déploiement automatique de l'infrastructure
- Exécute `tofu apply -auto-approve`
- Mise à jour de la Lambda function
- Affiche l'URL de l'API Gateway déployée

**Résultat**: Lambda function et API Gateway déployés automatiquement

---

### 2.3 Pull Request #2 - Test du Workflow CI

**Branche**: test-workflow  
**Objectif**: Tester le workflow app-tests.yml avec une erreur intentionnelle

**Changements**:
1. Modification de `app.js`: "Hello, World!" → "DevOps Labs!"
2. Création de la PR avec erreur intentionnelle (test qui échoue)
3. Correction du test pour correspondre à la nouvelle réponse
4. Merge après succès des tests

**Preuve**: PR #2 merged avec succès après correction

---

### 2.4 Pull Request #3 - Test du Pipeline CD Complet

**Branche**: deploy-lambda-sample  
**Objectif**: Tester le pipeline CD complet (plan + apply)

**Changements effectués**:
1. Modification du message de la Lambda function
2. Mise à jour de la documentation README_TD5.md
3. Création de la PR → workflow tofu-plan.yml exécuté
4. Merge vers main → workflow tofu-apply.yml exécuté

**Résultat**:
- Infrastructure déployée automatiquement
- Lambda function mise à jour
- API Gateway accessible publiquement

**Preuve**: PR #3 merged, infrastructure déployée avec succès

---

## Infrastructure Déployée

### Lambda Function
- **Nom**: Variable selon configuration
- **Runtime**: Node.js 20.x
- **Code source**: `td5/scripts/tofu/live/lambda-sample/src/index.js`
- **Intégration**: API Gateway

### API Gateway
- **Type**: HTTP API
- **Route**: GET /
- **Intégration**: Lambda Proxy
- **Accès**: Public

**Test de l'endpoint**:
```bash
curl https://<api-gateway-url>/
# Réponse attendue: Message de la Lambda function
```

---

## Modules OpenTofu Créés

### 1. Module state-bucket
- Création de bucket S3 avec versioning
- Configuration du chiffrement
- Gestion du cycle de vie

### 2. Module github-aws-oidc
- Configuration du OIDC provider GitHub
- Trust policy pour GitHub Actions
- Audience STS

### 3. Module gh-actions-iam-roles
- Création des 3 rôles IAM
- Policies attachées selon le principe du moindre privilège
- Trust relationships avec OIDC

### 4. Module lambda (copié de TD3)
- Déploiement de fonctions Lambda
- Configuration des variables d'environnement
- Gestion des logs CloudWatch

### 5. Module api-gateway (copié de TD3)
- Configuration HTTP API
- Routes et intégrations
- CORS si nécessaire

---

## Fichiers de Configuration Créés

### Backend Configuration
**Fichier**: `td5/scripts/tofu/live/lambda-sample/backend.tf`

Contenu:
```hcl
terraform {
  backend "s3" {
    bucket         = "samba-diallo-devops-tofu-state-2025"
    key            = "td5/lambda-sample/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "samba-diallo-devops-tofu-state-2025"
    encrypt        = true
  }
}
```

### Main Configuration
**Fichier**: `td5/scripts/tofu/live/lambda-sample/main.tf`

Utilise les modules locaux:
```hcl
module "lambda" {
  source = "../../modules/lambda"
  # ...
}

module "api_gateway" {
  source = "../../modules/api-gateway"
  # ...
}
```

---

## Tests Effectués

### Tests Unitaires (Jest)
- Tests de l'application sample-app
- Vérification des endpoints HTTP
- Validation des réponses

### Tests d'Infrastructure (OpenTofu)
**Fichier**: `td5/scripts/tofu/live/lambda-sample/deploy.tftest.hcl`

Tests:
1. Validation de la configuration OpenTofu
2. Déploiement de l'infrastructure
3. Vérification de l'endpoint API Gateway
4. Test de la réponse de la Lambda

---

## Sécurité

### Bonnes Pratiques Implémentées

1. **OIDC au lieu de clés statiques**
   - Pas de AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY dans GitHub
   - Authentification temporaire via OIDC
   - Principe du moindre privilège pour chaque rôle

2. **State Management Sécurisé**
   - State stocké dans S3 avec encryption
   - Versioning activé pour rollback possible
   - Locking avec DynamoDB pour éviter les conflits

3. **Secrets Management**
   - Pas de secrets hardcodés dans le code
   - Utilisation des GitHub Secrets pour les ARNs
   - Variables d'environnement pour la configuration

---

## Commits Principaux

### Commit Initial - Workflows CI
```
commit: <hash>
Message: "Add GitHub Actions workflows for CI testing"
Fichiers: .github/workflows/app-tests.yml, infra-tests.yml
```

### Commit - Infrastructure AWS
```
commit: <hash>
Message: "Setup AWS OIDC and IAM roles for GitHub Actions"
Fichiers: td5/scripts/tofu/live/ci-cd-permissions/
```

### Commit - Backend Configuration
```
commit: <hash>
Message: "Configure S3 backend for OpenTofu state"
Fichiers: td5/scripts/tofu/live/lambda-sample/backend.tf
```

### Commit - CD Workflows
```
commit: <hash>
Message: "Add tofu-plan and tofu-apply workflows"
Fichiers: .github/workflows/tofu-plan.yml, tofu-apply.yml
```

### Commit Final - Documentation
```
commit: 44e0d73
Message: "Remove emojis from TD5 README and fix structure"
Fichier: td5/README_TD5.md
```

---

## Vérifications Possibles

Pour vérifier que tout fonctionne:

### 1. Vérifier les Workflows GitHub
```bash
# Voir l'historique des workflows
gh run list --repo samba-diallo/Devops
```

### 2. Vérifier l'Infrastructure AWS
```bash
# S3 bucket
aws s3 ls s3://samba-diallo-devops-tofu-state-2025 --region us-east-2

# DynamoDB table
aws dynamodb describe-table --table-name samba-diallo-devops-tofu-state-2025 --region us-east-2

# IAM roles
aws iam get-role --role-name lambda-sample-tests
aws iam get-role --role-name lambda-sample-plan
aws iam get-role --role-name lambda-sample-apply

# OIDC provider
aws iam list-open-id-connect-providers
```

### 3. Vérifier les Déploiements
```bash
# Lister les fonctions Lambda
aws lambda list-functions --region us-east-2

# Lister les APIs Gateway
aws apigatewayv2 get-apis --region us-east-2
```

---

## Conclusion

Le TD5 a été complété avec succès. Tous les objectifs ont été atteints:

1. Configuration CI pour tester automatiquement l'application
2. Configuration CI pour tester automatiquement l'infrastructure
3. Configuration AWS OIDC pour authentification sécurisée
4. Création de 3 rôles IAM avec permissions appropriées
5. Backend S3 + DynamoDB pour le state management
6. Pipeline CD avec tofu-plan sur PRs
7. Pipeline CD avec tofu-apply après merge
8. Tests avec 2 Pull Requests (PR #2 et PR #3)
9. Documentation complète sans emojis

**Infrastructure AWS créée**:
- 1 S3 bucket (state)
- 1 DynamoDB table (locking)
- 1 OIDC provider
- 3 IAM roles
- Lambda function + API Gateway (via CD pipeline)

**Workflows GitHub Actions**:
- app-tests.yml (CI - application)
- infra-tests.yml (CI - infrastructure)
- tofu-plan.yml (CD - plan)
- tofu-apply.yml (CD - deploy)

Le projet suit les meilleures pratiques DevOps modernes avec authentification sécurisée, tests automatisés, et déploiement continu.
