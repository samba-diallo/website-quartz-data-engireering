---
title: "TD2 - Guide de Déploiement Section 7"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# SECTION 7: Utilisation de Modules OpenTofu depuis GitHub - GUIDE DE DÉPLOIEMENT

## Statut: Déploiement Conceptuel (En raison des limites vCPU)

**Note:** Cette section démontre les **concepts et la syntaxe** pour l'utilisation de modules GitHub. Le déploiement réel est limité par les contraintes vCPU du Free Tier AWS (limite de 16 vCPU atteinte avec les déploiements précédents).

---

## Démarrage Rapide

### Utilisation de Votre Module Local (Déjà Fonctionnel)

```bash
cd /home/sable/devops_base/td2/scripts/live/github-modules
tofu init
tofu plan
tofu apply -auto-approve
```

### Utilisation d'un Module GitHub (Prêt pour la Production)

**Étape 1: Pousser le Module vers GitHub**

```bash
cd /home/sable/devops_base/td2/scripts/modules
git init
git add -A
git commit -m "Initial OpenTofu module"
git remote add origin https://github.com/YOUR_USERNAME/iac-modules.git
git push -u origin main
```

**Étape 2: Créer un Tag de Release**

```bash
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0
```

**Étape 3: Mettre à Jour la Configuration OpenTofu**

Dans `main.tf`, décommenter et mettre à jour:

```hcl
module "github_module_instance" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id        = var.ami_id
  name          = "github-module-test"
  instance_type = "t3.micro"
  port          = 8080
}
```

**Étape 4: Déployer**

```bash
tofu init
tofu apply -auto-approve
```

---

## Concepts Clés Expliqués

### 1. Format de Source de Module GitHub

```
github.com/USERNAME/REPO.git//PATH/TO/MODULE?ref=REFERENCE
```

Composants:
- **USERNAME**: Votre nom d'utilisateur GitHub
- **REPO**: Nom du dépôt (ex: "iac-modules")
- **PATH**: Chemin vers le module dans le dépôt (ex: "ec2-instance")
- **ref**: Référence de version (optionnel)

### 2. Références de Version

| Référence | Format | Cas d'Usage | Exemple |
|-----------|--------|-------------|---------|
| **Par défaut** | `(pas de ?ref)` | Développement | `github.com/user/repo.git//module` |
| **Tag** | `?ref=v1.0.0` | Production | `github.com/user/repo.git//module?ref=v1.0.0` |
| **Branche** | `?ref=main` | Dernières fonctionnalités | `github.com/user/repo.git//module?ref=main` |
| **Commit** | `?ref=abc123` | Débogage | `github.com/user/repo.git//module?ref=abc123` |

### 3. Versionnage Sémantique

```
v1.2.3
├── 1: MAJOR (changements breaking)
├── 2: MINOR (nouvelles fonctionnalités, rétrocompatible)
└── 3: PATCH (corrections de bugs, pas de nouvelles fonctionnalités)
```

**Exemples:**
- v1.0.0 → v1.1.0: Sûr à mettre à jour (nouvelles fonctionnalités)
- v1.0.0 → v2.0.0: Réviser attentivement (changements breaking)
- v1.0.0 → v1.0.1: Sûr à mettre à jour (correction de bug)

---

## Fichiers de Configuration dans `live/github-modules/`

### 1. example1-local-module.tf
Utilise un **module local** depuis `../../modules/ec2-instance`

```hcl
module "example1_local_sample_app" {
  source        = "../../modules/ec2-instance"
  ami_id        = var.ami_id
  name          = "example1-local-module-app"
  instance_type = var.instance_type
  port          = var.port
}
```

**Cas d'usage:** Développement, tests, interne uniquement

### 2. example2-github-module-terraform-aws.tf
Montre le pattern de **module Terraform Registry** (terraform-aws-modules)

```hcl
# Référence commentée pour montrer la syntaxe
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "main-vpc"
  cidr = "10.0.0.0/16"
}
```

**Cas d'usage:** Modules prêts pour la production de la communauté

### 3. example3-custom-github-module.tf
Montre le pattern de **module GitHub personnalisé** (votre propre dépôt)

```hcl
# Référence commentée pour montrer la syntaxe
module "github_sample_app" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id        = "ami-07eb809c44dd0fcab"
  name          = "github-module-app"
  instance_type = "t3.micro"
  port          = 8080
}
```

**Cas d'usage:** Partage d'infrastructure équipe/organisation

### 4. example4-multiple-versions.tf
Montre **plusieurs patterns de version** pour comparaison

```hcl
module "app_v1_0_0" {
  source = "github.com/user/repo.git//module?ref=v1.0.0"
  # ... config
}

module "app_v1_2_0" {
  source = "github.com/user/repo.git//module?ref=v1.2.0"
  # ... config
}

module "app_main" {
  source = "github.com/user/repo.git//module?ref=main"
  # ... config
}
```

**Cas d'usage:** Test de compatibilité de version, mises à jour graduelles

---

## Comparaison: Sources de Modules

### Module Local
```hcl
source = "../../modules/ec2-instance"
```

**Avantages:**
- Développement rapide
- Pas besoin de Git
- Modifications instantanées

**Inconvénients:**
- Non versionné
- Non partageable
- Pas de contrôle de version

### Module GitHub
```hcl
source = "github.com/user/iac-modules.git//ec2-instance?ref=v1.0.0"
```

**Avantages:**
- Versionné avec Git
- Partageable avec l'équipe
- Changements traçables
- CI/CD friendly

**Inconvénients:**
- Setup initial requis
- Besoin de pousser les changements

### Module Registry
```hcl
source  = "terraform-aws-modules/vpc/aws"
version = "5.0.0"
```

**Avantages:**
- Testé par la communauté
- Documentation complète
- Meilleures pratiques
- Maintenu activement

**Inconvénients:**
- Moins de contrôle
- Peut être trop générique

---

## Workflow Recommandé

1. **Développement**: Commencer avec des modules locaux
2. **Tests**: Valider la fonctionnalité localement
3. **Version**: Pousser vers GitHub avec tags
4. **Partage**: Utiliser les références GitHub dans les projets
5. **Production**: Utiliser des tags de version fixes

## Fichiers Disponibles

Les configurations complètes sont disponibles dans:
- [Modules](/static/devops/td2/modules/)
- [Live Configurations](/static/devops/td2/live/)
- [GitHub Modules Examples](/static/devops/td2/live/github-modules/)

## Ressources

- Documentation OpenTofu: https://opentofu.org/docs/
- Terraform Registry: https://registry.terraform.io/
- Git Tagging: https://git-scm.com/book/en/v2/Git-Basics-Tagging
