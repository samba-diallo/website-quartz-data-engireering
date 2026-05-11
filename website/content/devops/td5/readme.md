---
title: "TD5 - CI/CD avec Kubernetes"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# TD5: Continuous Integration (CI) and Continuous Delivery (CD) with Kubernetes

**Auteur:** Samba DIALLO , Mouhamed DIOP
**Date:** 7 décembre 2025  
**Repository:** samba-diallo/Devops

## Objectifs

Ce TD couvre:
- Configuration du CI avec tests automatisés (application et infrastructure)
- Configuration de l'authentification OIDC avec AWS
- Création d'un pipeline de déploiement automatisé avec GitHub Actions et OpenTofu
- Compréhension et application de différentes stratégies de déploiement
- Exploration du concept GitOps avec Flux

## Prérequis

- Compte GitHub
- Compte AWS
- Cluster Kubernetes local (Docker Desktop ou Minikube)
- Outils installés: Git, Docker, kubectl, OpenTofu, npm, Node.js, aws-cli, flux

---

## Part 1: Continuous Integration (CI)

### Section 1.1: Introduction au CI

Le CI (Continuous Integration) consiste à fusionner fréquemment le code dans la branche principale (`main`), idéalement plusieurs fois par jour. Cela permet une détection et résolution précoce des problèmes d'intégration.

**Principes clés du CI:**
- **Trunk-based development:** Travailler sur une seule branche principale avec des branches de fonctionnalité courtes
- **Self-testing build:** Tests automatisés exécutés après chaque commit
- **Serveur CI:** Automatise le processus de build et de test

### Section 1.2: Tests Automatisés de l'Application avec GitHub Actions

**Objectif:** Configurer un workflow GitHub Actions pour exécuter automatiquement les tests de l'application Node.js après chaque push.

#### Étapes réalisées:

1. **Préparation du projet:**
```bash
cd ~/devops_base
git checkout main
git pull origin main
```

2. **Création du workflow GitHub Actions:**

Fichier créé: `.github/workflows/app-tests.yml`

```yaml
name: Sample App Tests

on: push

jobs:
  sample_app_tests:
    name: "Run Tests Using Jest"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        working-directory: td5/scripts/sample-app
        run: npm install

      - name: Run tests
        working-directory: td5/scripts/sample-app
        run: npm test
```

**Explication du workflow:**
- `name`: Nom du workflow
- `on: push`: Déclenche le workflow à chaque push sur n'importe quelle branche
- `jobs`: Définit les tâches à exécuter
- `runs-on: ubuntu-latest`: Spécifie l'environnement d'exécution (Ubuntu)
- `steps`: Séquence d'étapes à exécuter

3. **Test du workflow avec une erreur intentionnelle:**

```bash
# Créer une branche de test
git checkout -b test-workflow

# Modifier app.js pour introduire une erreur
# Changé "Hello, World!" en "DevOps Labs!"
git add td5/scripts/sample-app/app.js
git commit -m "Introduce intentional error"
git push origin test-workflow
```

4. **Création d'un Pull Request:**
- PR #2 créé: "Test workflow with intentional error"
- Le workflow a échoué car le test attendait "Hello, World!" mais l'app retournait "DevOps Labs!"

5. **Correction du test:**

```bash
# Modifier app.test.js pour correspondre à la nouvelle réponse
git add td5/scripts/sample-app/app.test.js
git commit -m "Update response text in test"
git push origin test-workflow
```

6. **Résultat:**
- Le workflow a réussi après la correction
- PR #2 fusionné avec succès (commit: 0ccf4af)

**Résultats:**
- Workflow GitHub Actions configuré et testé
- Tests automatisés fonctionnels
- Processus de CI validé avec un cycle erreur → correction → succès

### Section 1.3: Machine User Credentials et Automatically-Provisioned Credentials

Pour exécuter des tests d'infrastructure (OpenTofu) qui déploient des ressources AWS, il faut configurer l'authentification.

**Deux approches:**
1. **Machine User Credentials:** Compte utilisateur dédié pour l'automatisation avec permissions limitées
   - Inconvénients: gestion manuelle des credentials, credentials longue durée

2. **Automatically-Provisioned Credentials (OIDC):** Credentials générés dynamiquement avec durée de vie courte
   - Plus sécurisé et recommandé

### Section 1.4: Configuration OIDC avec AWS et GitHub Actions

**Objectif:** Configurer OIDC pour permettre à GitHub Actions de s'authentifier à AWS de manière sécurisée.

#### Étapes réalisées:

1. **Configuration des credentials AWS:**
```bash
aws configure
# AWS Access Key ID: [Votre clé]
# AWS Secret Access Key: [Votre clé secrète]
# Default region name: us-east-2
# Default output format: json
```

2. **Création du bucket S3 et table DynamoDB pour l'état OpenTofu:**

Fichier `td5/scripts/tofu/live/tofu-state/main.tf`:
```hcl
provider "aws" {
  region = "us-east-2"
}

module "state" {
  source = "../../modules/state-bucket"
  name   = "samba-diallo-devops-tofu-state-2025"
}
```

Déploiement:
```bash
cd td5/scripts/tofu/live/tofu-state
tofu init
tofu apply -auto-approve
```

**Résultat:**
- Bucket S3: `samba-diallo-devops-tofu-state-2025`
- Table DynamoDB: `samba-diallo-devops-tofu-state-2025`

3. **Création du provider OIDC dans AWS:**

Fichier `td5/scripts/tofu/live/ci-cd-permissions/main.tf`:
```hcl
provider "aws" {
  region = "us-east-2"
}

module "oidc_provider" {
  source = "../../modules/github-aws-oidc"
  provider_url = "https://token.actions.githubusercontent.com"
}

module "iam_roles" {
  source = "../../modules/gh-actions-iam-roles"
  
  name              = "lambda-sample"
  oidc_provider_arn = module.oidc_provider.oidc_provider_arn
  
  enable_iam_role_for_testing = true
  enable_iam_role_for_plan    = true
  enable_iam_role_for_apply   = true
  
  github_repo      = "samba-diallo/Devops"
  lambda_base_name = "lambda-sample"
  
  tofu_state_bucket         = "samba-diallo-devops-tofu-state-2025"
  tofu_state_dynamodb_table = "samba-diallo-devops-tofu-state-2025"
}
```

Déploiement:
```bash
cd td5/scripts/tofu/live/ci-cd-permissions
tofu init
tofu apply -auto-approve
```

**Résultat - Trois rôles IAM créés:**
- **lambda-sample-tests**: `arn:aws:iam::511211062907:role/lambda-sample-tests`
- **lambda-sample-plan**: `arn:aws:iam::511211062907:role/lambda-sample-plan`
- **lambda-sample-apply**: `arn:aws:iam::511211062907:role/lambda-sample-apply`

4. **Création du workflow GitHub Actions pour les tests d'infrastructure:**

Fichier `.github/workflows/infra-tests.yml`:
```yaml
name: Infrastructure Tests

on: push

jobs:
  opentofu_test:
    name: "Run OpenTofu tests"
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v3

      - uses: aws-actions/configure-aws-credentials@v3
        with:
          role-to-assume: arn:aws:iam::511211062907:role/lambda-sample-tests
          role-session-name: tests-${{ github.run_number }}-${{ github.actor }}
          aws-region: us-east-2

      - uses: opentofu/setup-opentofu@v1

      - name: Tofu Test
        env:
          TF_VAR_name: lambda-sample-${{ github.run_id }}
        working-directory: td5/scripts/tofu/live/lambda-sample
        run: |
          tofu init -backend=false -input=false
          tofu test -verbose
```

**Explication du workflow:**
- `permissions`: Permissions nécessaires pour OIDC (id-token: write)
- `configure-aws-credentials@v3`: Action qui utilise OIDC pour s'authentifier à AWS
- `role-to-assume`: ARN du rôle IAM créé précédemment
- `TF_VAR_name`: Nom unique pour chaque run de test (utilise github.run_id)
- `-backend=false`: Pas besoin du backend pour les tests

**Avantages de l'approche OIDC:**
-  Pas de credentials statiques stockés dans GitHub
-  Credentials temporaires générés à chaque run
-  Plus sécurisé que les Access Keys
-  Permissions finement contrôlées par rôle IAM

---

## Part 2: Continuous Delivery (CD)

### Section 2.1: Stratégies de Déploiement

Comparaison des différentes stratégies:

| Stratégie | Interruption | Applications sans état | Applications avec état |
|-----------|--------------|------------------------|------------------------|
| **Downtime Deployment** | Oui | Supporté | Supporté |
| **Progressive sans remplacement** | Non | Supporté | Alterné entre versions |
| **Progressive avec remplacement** | Non | Supporté | Supporté |
| **Blue/Green** | Non | Supporté | Non supporté |
| **Canary** | Non | Supporté | Supporté |
| **Feature Toggles** | Non | Supporté | Supporté |
| **Promotion** | Variable | Supporté | Supporté |

**Recommandations:**
- **Applications sans état:** Blue/green si possible, sinon progressive sans remplacement
- **Applications avec état:** Progressive avec remplacement
- **Migrations de données complexes:** Downtime planifié peut être plus simple

**Stratégies complémentaires:**
- **Canary:** Réduit l'impact des déploiements défectueux en déployant initialement sur une seule instance
- **Feature Toggles:** Permet de déployer du code sans activer les nouvelles fonctionnalités
- **Promotion:** Déploie le code à travers plusieurs environnements (dev, staging, prod)

### Section 2.2: Pipeline de Déploiement Automatisé

**Objectif:** Configurer un pipeline de déploiement pour le module lambda-sample qui s'exécute sur les pull requests (plan) et après fusion (apply).

#### Étapes réalisées:

1. **Préparation des modules OpenTofu:**

Copie des modules lambda et api-gateway depuis td3:
```bash
cp -r td3/scripts/tofu/modules/lambda td5/scripts/tofu/modules/
cp -r td3/scripts/tofu/modules/api-gateway td5/scripts/tofu/modules/
```

Mise à jour de `td5/scripts/tofu/live/lambda-sample/main.tf`:
```hcl
provider "aws" {
  region = "us-east-2"
}

module "function" {
  source = "../../modules/lambda"
  name = var.name
  src_dir = "${path.module}/src"
  runtime = "nodejs20.x"
  handler = "index.handler"
  memory_size = 128
  timeout     = 5
  environment_variables = {
    NODE_ENV = "production"
  }
}

module "gateway" {
  source = "../../modules/api-gateway"
  name = var.name
  function_arn       = module.function.function_arn
  api_gateway_routes = ["GET /"]
}
```

Configuration du backend S3 dans `td5/scripts/tofu/live/lambda-sample/backend.tf`:
```hcl
terraform {
  backend "s3" {
    bucket         = "samba-diallo-devops-tofu-state-2025"
    key            = "td5/tofu/live/lambda-sample"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "samba-diallo-devops-tofu-state-2025"
  }
}
```

2. **Workflow tofu-plan.yml:**

Fichier `.github/workflows/tofu-plan.yml`:
```yaml
name: Tofu Plan

on:
  pull_request:
    branches: ["main"]
    paths: ["td5/scripts/tofu/live/lambda-sample/**"]

jobs:
  plan:
    name: "Tofu Plan"
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v3

      - uses: aws-actions/configure-aws-credentials@v3
        with:
          role-to-assume: arn:aws:iam::511211062907:role/lambda-sample-plan
          role-session-name: plan-${{ github.run_number }}-${{ github.actor }}
          aws-region: us-east-2

      - uses: opentofu/setup-opentofu@v1

      - name: tofu plan
        id: plan
        working-directory: td5/scripts/tofu/live/lambda-sample
        run: |
          tofu init -no-color -input=false
          tofu plan -no-color -input=false -lock=false

      - uses: peter-evans/create-or-update-comment@v4
        if: always()
        env:
          RESULT_EMOJI: ${{ steps.plan.outcome == 'success' && '' || '' }}
        with:
          issue-number: ${{ github.event.pull_request.number }}
          body: |
            ## ${{ env.RESULT_EMOJI }} `tofu plan` output
            ```
            ${{ steps.plan.outputs.stdout }}
            ```
```

**Fonctionnement:**
- Se déclenche sur les pull requests vers `main`
- S'authentifie avec AWS via OIDC (rôle `lambda-sample-plan`)
- Exécute `tofu plan` pour prévisualiser les changements
- Publie automatiquement le résultat dans un commentaire du PR

3. **Workflow tofu-apply.yml:**

Fichier `.github/workflows/tofu-apply.yml`:
```yaml
name: Tofu Apply

on:
  push:
    branches: ["main"]
    paths: ["td5/scripts/tofu/live/lambda-sample/**"]

jobs:
  apply:
    name: "Tofu Apply"
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v3

      - uses: aws-actions/configure-aws-credentials@v3
        with:
          role-to-assume: arn:aws:iam::511211062907:role/lambda-sample-apply
          role-session-name: apply-${{ github.run_number }}-${{ github.actor }}
          aws-region: us-east-2

      - uses: opentofu/setup-opentofu@v1

      - name: tofu apply
        id: apply
        working-directory: td5/scripts/tofu/live/lambda-sample
        run: |
          tofu init -no-color -input=false
          tofu apply -no-color -input=false -lock-timeout=60m -auto-approve

      - uses: jwalton/gh-find-current-pr@master
        id: find_pr
        with:
          state: all

      - uses: peter-evans/create-or-update-comment@v4
        if: steps.find_pr.outputs.number
        env:
          RESULT_EMOJI: ${{ steps.apply.outcome == 'success' && '' || '' }}
        with:
          issue-number: ${{ steps.find_pr.outputs.number }}
          body: |
            ## ${{ env.RESULT_EMOJI }} `tofu apply` output
            ```
            ${{ steps.apply.outputs.stdout }}
            ```
```

**Fonctionnement:**
- Se déclenche après fusion d'un PR sur `main`
- S'authentifie avec AWS via OIDC (rôle `lambda-sample-apply`)
- Exécute `tofu apply -auto-approve` pour déployer automatiquement
- Publie le résultat du déploiement dans le PR associé

4. **Test du pipeline:**

Création du PR #3: "TD5: Deploy Lambda sample with CI/CD pipeline"
- Branche: `deploy-lambda-sample`
- Modification: Message de la fonction Lambda changé
- Le workflow `tofu-plan` s'exécute automatiquement
- Après fusion, le workflow `tofu-apply` déploiera automatiquement

**Avantages du pipeline CD:**
-  Déploiements automatisés après fusion
-  Revue des changements infrastructure avant déploiement
-  Traçabilité complète via GitHub Actions
-  Rollback facile via Git revert
-  Pas d'intervention manuelle nécessaire

---

## Exercice Pratique (Optionnel)

### Détection automatique des changements OpenTofu

**Objectif:** Améliorer le pipeline pour détecter automatiquement les changements dans n'importe quel dossier contenant du code OpenTofu.

**Suggestions d'amélioration:**

1. **Détection automatique des dossiers modifiés:**
   - Utiliser l'action `changed-files` pour détecter les dossiers OpenTofu modifiés
   - Exécuter `tofu plan` et `tofu apply` automatiquement pour chaque dossier détecté
   - Au lieu de cibler uniquement `lambda-sample`, supporter tous les modules

2. **Exécution concurrente avec matrix strategy:**
   - Si un PR modifie plusieurs dossiers OpenTofu
   - Utiliser une stratégie matrix dans GitHub Actions
   - Exécuter plan/apply en parallèle sur tous les dossiers modifiés
   - Réduire le temps d'exécution total

**Exemple de workflow amélioré:**
```yaml
jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      folders: ${{ steps.changed-files.outputs.all_changed_files }}
    steps:
      - uses: actions/checkout@v3
      - id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          files: |
            td5/scripts/tofu/live/**/*.tf
  
  plan:
    needs: detect-changes
    if: needs.detect-changes.outputs.folders != ''
    strategy:
      matrix:
        folder: ${{ fromJSON(needs.detect-changes.outputs.folders) }}
    runs-on: ubuntu-latest
    steps:
      - name: Plan for ${{ matrix.folder }}
        run: |
          tofu -chdir=${{ matrix.folder }} plan
```

---

## Résumé des Commits

1. **Commit 8821e2c:** Add GitHub Actions workflow for sample app tests
2. **Commit 0ccf4af:** Merge PR #2 - Test workflow with error correction
3. **Commit 159296a:** Add TD5 README with CI/CD documentation
4. **Commit 3ced3d8:** TD5: Configure OIDC with AWS and infrastructure tests workflow
   - Created S3 bucket: samba-diallo-devops-tofu-state-2025
   - Created DynamoDB table: samba-diallo-devops-tofu-state-2025
   - Configured GitHub OIDC provider
   - Created 3 IAM roles (tests, plan, apply)
   - Added infrastructure tests workflow
5. **Commit c4c64cc:** Update TD5 README with OIDC configuration steps and results
6. **Commit 409de81:** TD5: Add CD workflows for OpenTofu deployment
   - Created tofu-plan.yml workflow for PR reviews
   - Created tofu-apply.yml workflow for auto-deployment
   - Added lambda and api-gateway modules from td3
   - Updated lambda-sample to use local modules
7. **PR #3 créé:** TD5: Deploy Lambda sample with CI/CD pipeline
   - Testing the complete CI/CD pipeline
   - Demonstrates tofu-plan on PR and tofu-apply after merge

---

## Commandes Utiles

### GitHub Actions
```bash
# Voir les workflows
gh workflow list

# Voir les runs d'un workflow
gh run list --workflow=app-tests.yml

# Voir les logs d'un run
gh run view <run-id> --log
```

### OpenTofu
```bash
# Initialiser avec backend
tofu init

# Planifier les changements
tofu plan

# Appliquer les changements
tofu apply

# Tester l'infrastructure
tofu test
```

### Kubernetes
```bash
# Vérifier l'état du cluster
kubectl cluster-info

# Lister les pods
kubectl get pods

# Déployer une application
kubectl apply -f deployment.yaml
```

---

## Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenTofu Documentation](https://opentofu.org/docs/)
- [AWS IAM OIDC Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)

---

## Conclusion

Ce TD5 a permis de:
-  Mettre en place un pipeline CI/CD complet avec GitHub Actions
-  Comprendre les principes du CI et les tests automatisés
-  Configurer l'authentification OIDC avec AWS (plus sécurisé que les Access Keys)
-  Créer des workflows automatisés pour plan et apply
-  Déployer automatiquement une fonction Lambda sur AWS
-  Explorer différentes stratégies de déploiement (Blue/Green, Canary, etc.)

**Résultats concrets:**
- 4 workflows GitHub Actions fonctionnels
- 1 bucket S3 et 1 table DynamoDB pour l'état partagé
- 3 rôles IAM avec OIDC pour l'authentification sécurisée
- Pipeline CD automatique: PR → Plan → Merge → Deploy
- Lambda déployée automatiquement sur AWS

Les compétences acquises sont essentielles pour l'automatisation et la livraison continue dans un environnement DevOps moderne.
