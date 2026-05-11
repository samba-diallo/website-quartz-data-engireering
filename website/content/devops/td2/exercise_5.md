---
title: "TD2 - Exercice 5: Construction Packer Multiple"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Exercice 5: Que se passe-t-il lors d'une double exécution de Packer Build?

Lorsque vous exécutez `packer build` une seconde fois avec le même modèle, Packer crée une NOUVELLE AMI avec un ID DIFFÉRENT, il ne réutilise pas l'existante.

## Observations Clés

### 1. IDs d'AMI Différents
- Première construction: ami-07eb809c44dd0fcab
- Seconde construction: ami-079a315e32554235f

### 2. Noms Différents (En raison du Timestamp)
Le paramètre ami_name utilise formatdate() avec timestamp():

```hcl
ami_name = "sample-app-packer-${formatdate("YYYY-MM-DD-hhmm-ss", timestamp())}"
```

- Première construction: sample-app-packer-2025-11-26-2154-31
- Seconde construction: sample-app-packer-2025-11-26-2200-11

### 3. Dates de Création Différentes
- Première AMI créée: 2025-11-26T21:56:19.000Z
- Seconde AMI créée: 2025-11-26T22:02:04.000Z

## Pourquoi C'est Important

- Packer génère un nom d'AMI UNIQUE à chaque fois en utilisant le timestamp
- AWS autorise plusieurs AMIs avec des noms différents, donc aucun conflit ne se produit
- Chaque construction est indépendante et crée une AMI fraîche
- Les deux anciennes AMIs restent dans votre compte AWS (vous devrez peut-être les nettoyer pour économiser des coûts)

## Idempotence dans Packer

Contrairement à Terraform ou Ansible, Packer n'est PAS idempotent par défaut:
- **Terraform**: Exécution deux fois avec la même config → aucun changement (idempotent)
- **Packer**: Exécution deux fois avec la même config → crée 2 AMIs différentes (non idempotent)

Pour rendre Packer idempotent, vous devriez:
1. Utiliser un ami_name fixe (sans timestamp) → mais alors la seconde construction échoue si l'AMI existe
2. Vérifier si l'AMI existe avant de construire
3. Utiliser une stratégie de nommage avec des numéros de version et nettoyer les anciennes versions

## Approche du Modèle Actuel

Le modèle actuel utilise timestamp() pour assurer des noms UNIQUES, faisant que chaque construction crée une nouvelle AMI.
Ceci est utile pour les pipelines CI/CD où vous voulez suivre différentes versions.

## Recommandation de Nettoyage

Après plusieurs constructions, nettoyez les anciennes AMIs:

```bash
aws ec2 deregister-image --image-id ami-07eb809c44dd0fcab --region us-east-2 --profile labs-devops_diallo
aws ec2 deregister-image --image-id ami-079a315e32554235f --region us-east-2 --profile labs-devops_diallo
```

**Note**: Supprimez également les snapshots associés pour éviter les coûts de stockage.

## Points Clés à Retenir

- Packer crée toujours une nouvelle AMI, même avec la même configuration
- L'utilisation de timestamps garantit l'unicité mais empêche l'idempotence
- La gestion des AMIs anciennes est importante pour le contrôle des coûts
- Pour la production, considérez une stratégie de versionnage et de nettoyage
