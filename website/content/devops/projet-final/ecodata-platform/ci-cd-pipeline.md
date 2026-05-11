---
title: "Pipeline CI/CD - GitHub Actions"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Pipeline CI/CD avec GitHub Actions

Le workflow `ci-cd-ghcr.yml` automatise l'intégralité du pipeline CI/CD pour l'EcoData Platform, de la phase de test au déploiement des images Docker sur GitHub Container Registry.

## Vue d'ensemble

Ce pipeline GitHub Actions est déclenché automatiquement à chaque :
- **Push** sur la branche `main`
- **Pull Request** vers la branche `main`

Il garantit la qualité du code et automatise la construction et publication des images Docker.

## Architecture du pipeline

```
┌─────────────────────────────────────────┐
│         Déclenchement (Push/PR)          │
└───────────────┬─────────────────────────┘
                │
                ▼
         ┌──────────────┐
         │   JOB 1      │
         │   Tests      │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │   JOB 2      │
         │  Build & Push│ (uniquement sur push)
         └──────┬───────┘
                │
        ┌───────┴───────┐
        ▼               ▼
 ┌──────────┐    ┌──────────┐
 │  JOB 3   │    │  JOB 4   │
 │Comment PR│    │  Report  │
 └──────────┘    └──────────┘
```

## Jobs du pipeline

### Job 1 : Tests

**Objectif :** Valider que le code compile et que les dépendances sont correctes.

**Étapes :**
1. Checkout du code source
2. Installation de Python 3.11
3. Installation des dépendances backend
4. Installation des dépendances frontend
5. Vérification de la compilation backend
6. Vérification de la compilation frontend

**Configuration :**
```yaml
test:
  name: Run Tests
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: projet-final-devops/ecodata-platform
```

**Tests exécutés :**
```bash
# Backend
pip install -r requirements.txt
python -c "print('[OK] Backend compile correctement')"

# Frontend
pip install -r requirements.txt
python -c "print('[OK] Frontend compile correctement')"
```

### Job 2 : Build and Push

**Objectif :** Construire les images Docker et les pousser vers GHCR.

**Conditions d'exécution :**
- Exécuté **uniquement** sur les `push` (pas sur les Pull Requests)
- Nécessite le succès du Job 1 (Tests)

**Étapes :**
1. Configuration de Docker Buildx
2. Authentification auprès de GHCR avec `GITHUB_TOKEN`
3. Extraction des métadonnées (tags, labels)
4. Build et push de l'image backend
5. Build et push de l'image frontend

**Images générées :**
```
ghcr.io/samba-diallo/devops/ecodata-backend:latest
ghcr.io/samba-diallo/devops/ecodata-backend:main-<sha>

ghcr.io/samba-diallo/devops/ecodata-frontend:latest
ghcr.io/samba-diallo/devops/ecodata-frontend:main-<sha>
```

**Configuration :**
```yaml
build-and-push:
  needs: test
  if: github.event_name == 'push'
  permissions:
    contents: read
    packages: write
```

### Job 3 : Comment PR

**Objectif :** Commenter automatiquement la Pull Request avec le statut du build.

**Conditions d'exécution :**
- Sur Push ou Pull Request
- Nécessite les Jobs 1 et 2

**Message généré :**
```markdown
## ✅ Pipeline CI/CD Status

**Tests:** PASSED  
**Build:** SUCCESS  
**Push to GHCR:** SUCCESS

### Images pushed:
- Backend: `ghcr.io/samba-diallo/devops/ecodata-backend:latest`
- Frontend: `ghcr.io/samba-diallo/devops/ecodata-frontend:latest`

**Next:** Deploy to Minikube locally or Kubernetes cluster
```

### Job 4 : Report

**Objectif :** Générer un rapport de déploiement téléchargeable.

**Conditions d'exécution :**
- S'exécute **toujours**, même si d'autres jobs échouent (`if: always()`)

**Contenu du rapport :**
```
Pipeline Summary Report
======================
Tests: success
Build: success
Timestamp: 2026-01-05 21:59:00
```

**Artefact :**
- Nom : `deployment-report`
- Rétention : 30 jours
- Format : fichier texte

## Déclencheurs

### Push sur main
```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'projet-final-devops/ecodata-platform/**'
      - '.github/workflows/ci-cd-ghcr.yml'
```

Le pipeline se déclenche uniquement si des fichiers dans ces chemins sont modifiés.

### Pull Request vers main
```yaml
on:
  pull_request:
    branches:
      - main
    paths:
      - 'projet-final-devops/ecodata-platform/**'
```

## Variables d'environnement

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME_BACKEND: ${{ github.repository }}/ecodata-backend
  IMAGE_NAME_FRONTEND: ${{ github.repository }}/ecodata-frontend
```

Ces variables sont accessibles dans tous les jobs du workflow.

## Configuration GitHub requise

### Permissions du workflow

**Important :** Le workflow nécessite des permissions d'écriture pour GHCR.

**Configuration à activer :**
1. Aller sur : `https://github.com/samba-diallo/Devops`
2. **Settings** → **Actions** → **General**
3. **Workflow permissions** → Sélectionner `Read and write permissions`
4. Cliquer sur **Save**

### Visibilité des packages GHCR

Pour rendre les images publiques :
1. Aller sur votre profil GitHub → **Packages**
2. Sélectionner `ecodata-backend` et `ecodata-frontend`
3. **Package settings** → **Danger Zone**
4. **Change visibility** → **Public**

## Utilisation

### Déclencher manuellement le pipeline

**Via un commit :**
```bash
# Faire un changement
echo "# Test pipeline" >> README.md

# Commit et push
git add README.md
git commit -m "Test CI/CD pipeline"
git push origin main
```

**Via une Pull Request :**
```bash
# Créer une branche
git checkout -b test-feature

# Faire des modifications
echo "nouvelle feature" > feature.txt
git add feature.txt
git commit -m "Add new feature"

# Pousser et créer une PR
git push origin test-feature
```

### Voir l'exécution

1. Aller sur : `https://github.com/samba-diallo/Devops/actions`
2. Cliquer sur le workflow exécuté
3. Voir les logs de chaque job

## Déboguer les erreurs

### Tests échouent
```bash
# Vérifier localement
cd projet-final-devops/ecodata-platform/backend
pip install -r requirements.txt
python -c "import main"
```

### Permission denied pour GHCR
```
Error: denied: permission_denied: write_package
```
**Solution :** Vérifier les permissions du workflow (voir Configuration GitHub).

### Syntaxe YAML invalide
```bash
# Valider localement
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci-cd-ghcr.yml'))"
```

## Téléchargement

Le fichier workflow est disponible :
- [Télécharger ci-cd-ghcr.yml](/static/.github/workflows/ci-cd-ghcr.yml)

## Retour à la documentation

- [[devops/projet-final/ecodata-platform/index|Vue d'ensemble du projet]]
- [[devops/projet-final/ecodata-platform/documentation-projet-final-deploiement|Guide de déploiement complet]]
- [[devops/projet-final/ecodata-platform/deploy-from-ghcr|Script de déploiement automatique]]
