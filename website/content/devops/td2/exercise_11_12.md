---
title: "TD2 - Exercices 11 et 12: Modules GitHub et Registry"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Section 7: Utilisation de Modules OpenTofu depuis GitHub

## Exercices 11 & 12

### Vue d'Ensemble
Cette section vous apprend à:
1. Utiliser des modules depuis des dépôts GitHub
2. Implémenter le contrôle de version avec les tags et branches Git
3. Trouver et utiliser des modules publics depuis Terraform Registry
4. Créer du code d'infrastructure réutilisable


## Exercice 11: Versionnage Git avec les Modules

### Objectif
Explorer les stratégies de versionnage pour les modules utilisant les tags et branches Git.

### Concepts

#### 1. Versionnage Sémantique
```
v1.2.3
├── 1: MAJOR (changements breaking)
├── 2: MINOR (nouvelles fonctionnalités, rétrocompatible)
└── 3: PATCH (corrections de bugs)
```

#### 2. Patterns de Source de Module

**Sans Version:**
```hcl
source = "github.com/username/repo.git//modules/ec2"
# Utilise: branche par défaut (main/master)
# Risque: Le code peut changer de manière inattendue
# Usage: Développement uniquement
```

**Avec Tag Git (RECOMMANDÉ):**
```hcl
source = "github.com/username/repo.git//modules/ec2?ref=v1.2.0"
# Utilise: Tag de version exacte
# Avantage: Reproductible, prévisible
# Usage: Environnements de production
```

**Avec Branche:**
```hcl
source = "github.com/username/repo.git//modules/ec2?ref=develop"
# Utilise: Branche spécifique
# Avantage: Dernières fonctionnalités de la branche
# Risque: Le code peut changer
# Usage: Développement, développement actif
```

**Avec SHA de Commit:**
```hcl
source = "github.com/username/repo.git//modules/ec2?ref=abc123def456"
# Utilise: Commit exact
# Avantage: Précision maximale
# Risque: Difficile à maintenir
# Usage: Débogage, scénarios de rollback
```

### Exercice Pratique

#### Étape 1: Préparer Votre Dépôt GitHub

Si vous n'avez pas de compte GitHub, créez-en un sur github.com.

```bash
# Créer un nouveau dépôt sur GitHub:
# 1. Aller sur github.com/new
# 2. Nom: "iac-modules"
# 3. Ajouter README
# 4. Créer le dépôt
```

#### Étape 2: Pousser Votre Module Local vers GitHub

```bash
# Dans votre espace de travail
cd /home/sable/devops_base/td2/scripts/modules

# Initialiser git (si pas déjà fait)
git init

# Ajouter tous les fichiers
git add -A
git commit -m "Initial module structure"

# Ajouter remote (remplacer YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/iac-modules.git

# Pousser vers la branche main
git branch -M main
git push -u origin main
```

#### Étape 3: Créer des Tags de Version

```bash
# Créer la première release
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0

# Créer la seconde release (avec améliorations)
git tag -a v1.1.0 -m "Add port parameterization"
git push origin v1.1.0

# Créer une branche de développement
git checkout -b develop
git push -u origin develop
```

#### Étape 4: Vérifier les Tags sur GitHub

```bash
# Voir tous les tags:
git tag -l
# Sortie:
# v1.0.0
# v1.1.0

# Voir les infos d'un tag spécifique:
git show v1.0.0
```

#### Étape 5: Tester Différentes Références de Version

Créer différents modules utilisant différentes versions:

```bash
cd /home/sable/devops_base/td2/scripts/live/github-modules
```

**Fichier: test-v1.0.0.tf**
```hcl
module "app_v1_0_0" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id        = var.ami_id
  name          = "app-v1-0-0"
  instance_type = "t3.micro"
  port          = 8080
}
```

**Fichier: test-v1.1.0.tf**
```hcl
module "app_v1_1_0" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.1.0"
  
  ami_id        = var.ami_id
  name          = "app-v1-1-0"
  instance_type = "t3.micro"
  port          = 9000
}
```

**Fichier: test-main.tf**
```hcl
module "app_main" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=main"
  
  ami_id        = var.ami_id
  name          = "app-main"
  instance_type = "t3.micro"
  port          = 8080
}
```

### Ce que Vous Apprenez

- Versionnage sémantique pour les modules
- Tagging Git pour les releases
- Versionnage basé sur les branches
- Références par SHA de commit
- Contraintes de version dans OpenTofu
- Gestion de modules prête pour la production

### Points Clés

1. **Toujours utiliser des tags de version en production** (?ref=v1.0.0)
2. **Utiliser des branches pour le développement** (?ref=develop)
3. **Documenter les changements de version** dans CHANGELOG.md
4. **Planifier les mises à jour soigneusement** - tester en staging d'abord
5. **Utiliser le versionnage sémantique** - attentes claires pour les changements

---

## Exercice 12: Utilisation de Modules Publics depuis Terraform Registry

### Objectif
Trouver et implémenter des modules prêts pour la production depuis des dépôts publics.

### Sources de Modules Populaires

#### 1. Terraform Registry (registry.terraform.io)
Registre officiel pour les modules Terraform et OpenTofu.

Modules courants:
- **terraform-aws-modules/ec2-instance/aws** - Instances EC2
- **terraform-aws-modules/vpc/aws** - VPC avec sous-réseaux
- **terraform-aws-modules/security-group/aws** - Groupes de sécurité
- **terraform-aws-modules/ecs/aws** - Clusters ECS

#### 2. Dépôts GitHub Publics

Options bien maintenues:
- hashicorp/terraform-aws-modules
- gruntwork-io/terraform-aws-modules
- cloudposse/terraform-aws-modules

### Exercice Pratique

#### Option A: Utiliser un Module Terraform Registry (LE PLUS FACILE)

**Étape 1: Trouver un Module**

Aller sur https://registry.terraform.io/modules et rechercher "security group"

Exemple: terraform-aws-modules/security-group/aws

**Étape 2: Lire la Documentation**

Le registre fournit:
- Description du module
- Variables d'entrée
- Valeurs de sortie
- Exemples d'utilisation

**Étape 3: Créer la Configuration**

```hcl
provider "aws" {
  region  = "us-east-2"
  profile = "labs-devops_diallo"
}

module "web_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.0.0"

  name        = "web-sg"
  description = "Security group for web server"
  vpc_id      = "vpc-xxxxxxxx"  # Votre VPC ID

  # Règles Ingress
  ingress_rules       = ["http-80-tcp", "https-443-tcp", "ssh-tcp"]
  ingress_cidr_blocks = ["0.0.0.0/0"]

  # Règle Egress
  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]

  tags = {
    Name = "web-server-sg"
  }
}

output "security_group_id" {
  value = module.web_security_group.security_group_id
}
```

### Modules Publics Recommandés

#### Pour EC2:
```hcl
source  = "terraform-aws-modules/ec2-instance/aws"
version = "5.0.0"
```

#### Pour VPC:
```hcl
source  = "terraform-aws-modules/vpc/aws"
version = "5.0.0"
```

#### Pour Security Groups:
```hcl
source  = "terraform-aws-modules/security-group/aws"
version = "5.0.0"
```

#### Pour RDS:
```hcl
source  = "terraform-aws-modules/rds/aws"
version = "5.0.0"
```

## Fichiers de Configuration Disponibles

Les exemples complets sont disponibles dans:
- [Modules locaux](/static/devops/td2/modules/)
- [Configurations GitHub modules](/static/devops/td2/live/github-modules/)

## Workflow Pratique

### Scénario: Partager un Module avec l'Équipe

#### Phase 1: Développement (Local)
```bash
# Créer le module localement
/modules/ec2-instance/
├── main.tf
├── variables.tf
├── outputs.tf
└── user-data.sh

# Tester localement
cd live/sample-app
tofu apply
```

#### Phase 2: Version (Git)
```bash
cd modules
git init
git add -A
git commit -m "Add ec2-instance module"
git remote add origin https://github.com/user/iac-modules.git
git push -u origin main
```

#### Phase 3: Release (Tag)
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

#### Phase 4: Partager (GitHub)
Les membres de l'équipe peuvent maintenant utiliser:
```hcl
module "app" {
  source = "github.com/user/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id = "ami-xxx"
  name   = "my-app"
}
```

## Bonnes Pratiques

1. Utiliser des tags de version pour la production
2. Tester les modules dans un environnement de staging
3. Documenter les changements dans CHANGELOG.md
4. Suivre le versionnage sémantique
5. Maintenir des exemples d'utilisation à jour
6. Fournir des valeurs par défaut raisonnables
7. Valider les entrées avec des contraintes
