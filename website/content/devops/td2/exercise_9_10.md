---
title: "TD2 - Exercices 9 et 10: Modules et Déploiement Scalable"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Exercice 9: Paramètrisation de Module - COMPLÉTÉ

## Objectif
Modifier le module pour accepter des paramètres additionnels (instance_type, port)

## Solution Implémentée

### Dans `/modules/ec2-instance/variables.tf`:

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "port" {
  description = "Port for HTTP traffic"
  type        = number
  default     = 8080
}
```

### Dans `/modules/ec2-instance/main.tf`:

```hcl
resource "aws_instance" "sample_app" {
  ami           = var.ami_id
  instance_type = var.instance_type  # Maintenant paramétré
  ...
}

resource "aws_security_group_rule" "allow_http_inbound" {
  from_port = var.port  # Maintenant paramétré
  to_port   = var.port
  ...
}
```

### Dans `/live/sample-app/main.tf`:

```hcl
module "sample_app_1" {
  source        = "../../modules/ec2-instance"
  ami_id        = var.ami_id
  name          = "sample-app-tofu-1"
  instance_type = var.instance_type  # Passage du paramètre
  port          = var.port           # Passage du paramètre
}
```

## Exemples d'Utilisation

### Valeurs par défaut (t3.micro, port 8080)
```bash
tofu apply -var="ami_id=ami-07eb809c44dd0fcab"
```

### Type d'instance et port personnalisés
```bash
tofu apply \
  -var="ami_id=ami-07eb809c44dd0fcab" \
  -var="instance_type=t3.small" \
  -var="port=9000"
```

### Ou utiliser un fichier tfvars
```bash
cat > terraform.tfvars << EOF
ami_id        = "ami-07eb809c44dd0fcab"
instance_type = "t3.small"
port          = 3000
EOF
tofu apply
```

## Avantages

- Module réutilisable à travers différentes configurations
- Différents ports pour différents environnements
- Différents types d'instances (optimisation des coûts)
- Module unique, multiples cas d'usage

---

# Exercice 10: Déploiement Scalable avec for_each - COMPLÉTÉ

## Objectif
Utiliser for_each pour déployer plusieurs instances sans duplication de code

## Implémentation

### Créer le fichier: `/live/sample-app-scalable/main.tf`

```hcl
provider "aws" {
  region  = "us-east-2"
  profile = "labs-devops_diallo"
}

variable "instances" {
  description = "Map of instances to create"
  type = map(object({
    name          = string
    instance_type = string
    port          = number
  }))
  default = {
    "prod-1" = {
      name          = "prod-app-1"
      instance_type = "t3.micro"
      port          = 8080
    }
    "prod-2" = {
      name          = "prod-app-2"
      instance_type = "t3.micro"
      port          = 8080
    }
    "prod-3" = {
      name          = "prod-app-3"
      instance_type = "t3.small"
      port          = 9000
    }
  }
}

variable "ami_id" {
  description = "The ID of the AMI to run."
  type        = string
}

module "sample_apps" {
  for_each      = var.instances
  source        = "../../modules/ec2-instance"
  ami_id        = var.ami_id
  name          = each.value.name
  instance_type = each.value.instance_type
  port          = each.value.port
}

output "instances" {
  description = "Details of all deployed instances"
  value = {
    for key, instance in module.sample_apps :
    key => {
      instance_id = instance.instance_id
      public_ip   = instance.public_ip
    }
  }
}
```

## Utilisation

### Déploiement avec instances par défaut (prod-1, prod-2, prod-3)
```bash
tofu apply -var="ami_id=ami-07eb809c44dd0fcab"
```

### Déploiement avec configuration personnalisée
```bash
tofu apply \
  -var="ami_id=ami-07eb809c44dd0fcab" \
  -var='instances={
    "dev-1" = {
      name          = "dev-app-1"
      instance_type = "t3.micro"
      port          = 8080
    }
    "staging-1" = {
      name          = "staging-app-1"
      instance_type = "t3.small"
      port          = 8081
    }
  }'
```

## Avantages du for_each

1. **Pas de duplication de code**: Un seul appel de module pour plusieurs instances
2. **Configuration déclarative**: Structure de données claire pour définir les instances
3. **Scalabilité**: Ajouter/supprimer des instances facilement
4. **Outputs structurés**: Récupération facile des IDs et IPs de toutes les instances
5. **Gestion d'état**: Terraform/OpenTofu gère chaque instance individuellement

## Comparaison: for_each vs count

### Avec count (ancien style):
```hcl
module "app" {
  count  = 3
  source = "..."
  name   = "app-${count.index}"  # app-0, app-1, app-2
}
```

**Problème**: Si vous supprimez app-1, Terraform doit recréer app-2 (devient app-1) et app-3 (devient app-2)

### Avec for_each (recommandé):
```hcl
module "app" {
  for_each = var.instances
  source   = "..."
  name     = each.value.name  # app-prod, app-dev, app-staging
}
```

**Avantage**: Chaque instance a une clé unique. Supprimer app-dev n'affecte pas les autres.

## Exemple de Sortie

Après `tofu apply`, vous obtenez:

```hcl
instances = {
  "prod-1" = {
    "instance_id" = "i-0abc123def456789"
    "public_ip"   = "18.219.45.67"
  }
  "prod-2" = {
    "instance_id" = "i-0def456abc123789"
    "public_ip"   = "18.220.56.78"
  }
  "prod-3" = {
    "instance_id" = "i-0123abc456def789"
    "public_ip"   = "18.221.67.89"
  }
}
```

## Cas d'Usage Pratiques

### Environnements multiples:
```hcl
instances = {
  "prod"    = { name = "app-prod",    type = "t3.medium", port = 443 }
  "staging" = { name = "app-staging", type = "t3.small",  port = 8443 }
  "dev"     = { name = "app-dev",     type = "t3.micro",  port = 8080 }
}
```

### Régions multiples (avec for_each imbriqué):
```hcl
regions = ["us-east-1", "us-west-2", "eu-west-1"]
```

### Applications microservices:
```hcl
services = {
  "api"      = { name = "service-api",      port = 8080 }
  "frontend" = { name = "service-frontend", port = 3000 }
  "worker"   = { name = "service-worker",   port = 9000 }
}
```

## Bonnes Pratiques

1. **Utiliser des clés significatives**: `"prod-api"` au lieu de `"instance1"`
2. **Définir des valeurs par défaut**: Pour faciliter les surcharges
3. **Documenter la structure**: Expliquer les champs requis dans les objets
4. **Valider les entrées**: Utiliser des contraintes de validation
5. **Utiliser des fichiers .tfvars**: Séparer la configuration par environnement

## Fichiers Disponibles

Les configurations complètes sont disponibles dans:
- [Module EC2 Instance](/static/devops/td2/modules/)
- [Configuration Live Sample App](/static/devops/td2/live/sample-app/)
- [Configuration Live Scalable](/static/devops/td2/live/sample-app-scalable/)
