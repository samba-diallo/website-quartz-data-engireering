---
title: "TD2 - Exercices 7 et 8: OpenTofu Multi-Instances"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Exercice 7: Recréation de Ressources après Destruction

## Question
Que se passe-t-il si vous exécutez `tofu apply` après avoir détruit les ressources?

## Réponse

Lorsque vous exécutez `tofu destroy` suivi de `tofu apply`, OpenTofu recrée toutes les ressources qui ont été détruites.

### Séquence d'Événements

1. **`tofu destroy`** supprime toutes les ressources (instance, security group)
   - Le fichier d'état est mis à jour pour refléter l'état détruit
   - Les ressources AWS sont supprimées

2. **`tofu apply`** après destruction:
   - Lit l'état Terraform actuel (maintenant vide)
   - Lit les fichiers de configuration (main.tf, variables.tf, etc.)
   - Compare l'état désiré (config) vs l'état actuel (AWS)
   - Constate que les ressources manquent
   - Crée de nouvelles ressources from scratch

### Différences Clés par rapport au Premier Apply

- **Nouvel Instance ID** sera différent
- **Nouvelle IP Publique** sera assignée
- **Nouvel ID de Security Group** sera créé
- Même configuration, mais ressources fraîches

### Exemple

**Premier déploiement:**
- Instance ID: `i-02538a44ef1b9c4d3`
- IP Publique: `18.220.53.35`
- Security Group: `sg-0a13eebec9656bbd1`

**Après destroy + apply:**
- Instance ID: `i-XXXXXXXXXXXXXXXX` (différent)
- IP Publique: `X.X.X.X` (différent - réassignée)
- Security Group: `sg-XXXXXXXXXXXXX` (différent)

### Pourquoi Cela Se Produit

AWS génère de nouveaux identifiants pour les ressources. Le fichier d'état suit quelles ressources appartiennent à quels IDs de ressources. Après destruction, l'état est propre, donc un nouveau apply crée des ressources complètement nouvelles.

---

# Exercice 8: Déploiement de Plusieurs Instances EC2

## Solution 1: Utilisation de for_each (Recommandé)

### Configuration

```hcl
variable "instance_names" {
  description = "Names for each instance"
  type        = list(string)
  default     = ["app-instance-1", "app-instance-2", "app-instance-3"]
}

resource "aws_instance" "sample_app_multi" {
  for_each               = toset(var.instance_names)
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")
  user_data_replace_on_change = true

  tags = {
    Name = each.value
  }
}

output "instance_ips" {
  description = "Public IPs of all instances"
  value       = {
    for name, instance in aws_instance.sample_app_multi :
    name => instance.public_ip
  }
}
```

### Utilisation

```bash
tofu apply -var="ami_id=ami-07eb809c44dd0fcab" \
  -var='instance_names=["prod-app-1", "prod-app-2"]'
```

## Solution 2: Utilisation de count

### Configuration

```hcl
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 3
}

resource "aws_instance" "sample_app_count" {
  count                  = var.instance_count
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")
  user_data_replace_on_change = true

  tags = {
    Name = "sample-app-${count.index + 1}"
  }
}

output "instance_ips" {
  description = "Public IPs of all instances"
  value       = aws_instance.sample_app_count[*].public_ip
}
```

### Utilisation

```bash
tofu apply -var="ami_id=ami-07eb809c44dd0fcab" -var="instance_count=3"
```

## Comparaison: for_each vs count

### for_each

**Avantages:**
- Meilleur nommage/identification
- Plus sûr lors de la suppression d'éléments (pas de décalage d'index)
- Plus lisible pour l'itération basée sur des clés

**Inconvénients:**
- Fonctionne uniquement avec des maps ou des sets
- Syntaxe plus complexe

### count

**Avantages:**
- Syntaxe plus simple
- Fonctionne pour l'itération numérique
- Bon pour les cas simples

**Inconvénients:**
- Fragile lors de la modification de listes (les indices se décalent)
- Moins lisible pour les scénarios complexes

## Bonne Pratique

**Recommandation:** Utilisez `for_each` pour les déploiements de production avec des identifiants significatifs.

## Test des Instances Multiples

Une fois déployées, testez toutes les instances:

```bash
for instance_ip in $(tofu output -json instance_ips | jq '.[]' -r); do
  echo "Testing $instance_ip..."
  curl http://$instance_ip:8080/
done
```

## Fichiers Disponibles

Les configurations complètes sont disponibles dans:
- [Modules EC2](/static/devops/td2/modules/)
- [Configurations Live](/static/devops/td2/live/)

Cela démontre la capacité d'OpenTofu à gérer l'infrastructure as code à l'échelle.
