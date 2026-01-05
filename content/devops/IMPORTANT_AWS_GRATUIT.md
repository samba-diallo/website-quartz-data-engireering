# IMPORTANT - Garder votre compte AWS GRATUIT

## Situation actuelle
Votre compte AWS a été automatiquement mis à niveau vers un forfait payant suite à la création d'AWS Organizations.

## Actions URGENTES réalisées

### 1. Ressources TD5 - DÉTRUITES ✓
- Lambda functions: Supprimées
- API Gateway: Supprimé
- S3 Bucket: Supprimé
- DynamoDB Table: Supprimée
- IAM Roles: Supprimés
- OIDC Provider: Supprimé

### 2. AWS Organizations - EN COURS DE SUPPRESSION
- Comptes STAGE et PROD: Marqués pour suppression
- Organisation: Sera supprimée automatiquement après fermeture des comptes (90 jours max)

## Comment RESTER GRATUIT

### Option 1: Utiliser uniquement le Free Tier
**Services gratuits pendant 12 mois:**
- EC2: 750 heures/mois d'instance t2.micro ou t3.micro
- S3: 5 GB de stockage
- Lambda: 1 million de requêtes/mois
- DynamoDB: 25 GB de stockage
- API Gateway: 1 million d'appels/mois

**IMPORTANT**: NE DÉPASSEZ PAS ces limites!

### Option 2: Simuler le TD6 SANS créer de vrais comptes AWS

Pour le TD6, au lieu de créer de vrais comptes AWS Organizations, vous pouvez:

1. **Utiliser OpenTofu Workspaces** (Partie 2 du TD6)
   - Créer des workspaces locaux: dev, stage, prod
   - Déployer dans le MÊME compte AWS mais avec des noms différents
   - Exemple: lambda-dev, lambda-stage, lambda-prod

2. **Utiliser Kubernetes localement** (Partie 3 du TD6)
   - Docker Desktop avec Kubernetes activé (GRATUIT)
   - Minikube (GRATUIT)
   - Kind (GRATUIT)
   - Pas besoin d'AWS pour cette partie!

## Actions à faire MAINTENANT

### 1. Vérifier qu'il n'y a plus de ressources actives
```bash
# Vérifier Lambda
aws lambda list-functions --region us-east-2

# Vérifier EC2
aws ec2 describe-instances --region us-east-2 --query 'Reservations[*].Instances[?State.Name==`running`]'

# Vérifier S3
aws s3 ls

# Vérifier DynamoDB
aws dynamodb list-tables --region us-east-2

# Vérifier API Gateway
aws apigatewayv2 get-apis --region us-east-2
```

### 2. Configurer des alertes de facturation

1. Allez sur: https://console.aws.amazon.com/billing/home#/
2. Cliquez sur "Billing preferences"
3. Activez "Receive Free Tier Usage Alerts"
4. Entrez votre email
5. Définissez un budget: $1/mois par exemple

### 3. Surveiller les coûts

- AWS Cost Explorer: https://console.aws.amazon.com/cost-management/home
- Vérifiez TOUS LES JOURS vos dépenses
- Si vous voyez des frais > $0.01, cherchez la ressource et supprimez-la

## TD6 - Plan d'action GRATUIT

### Partie 1: Multi-Comptes AWS ❌ ANNULÉE
**Raison**: Crée des comptes supplémentaires qui sortent du Free Tier

**Alternative**: Documentation théorique uniquement

### Partie 2: OpenTofu Workspaces ✅ POSSIBLE GRATUITEMENT
- Utiliser des workspaces dans votre compte unique
- Préfixer les ressources: dev-, stage-, prod-
- Tout reste dans le Free Tier

### Partie 3: Kubernetes Multi-Services ✅ 100% GRATUIT
- Docker Desktop + Kubernetes (local)
- Aucun coût AWS
- Frontend + Backend dans Kubernetes local

## Commandes de nettoyage d'urgence

Si vous voyez des frais apparaître:

```bash
# 1. Liste TOUTES les régions AWS
aws ec2 describe-regions --query 'Regions[*].RegionName' --output text

# 2. Pour CHAQUE région, vérifier les instances EC2
for region in $(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text); do
  echo "=== $region ==="
  aws ec2 describe-instances --region $region --query 'Reservations[*].Instances[?State.Name==`running`].[InstanceId]' --output text
done

# 3. Terminer TOUTES les instances
aws ec2 terminate-instances --instance-ids <ID> --region <REGION>

# 4. Supprimer TOUS les buckets S3
aws s3 ls | awk '{print $3}' | xargs -I {} aws s3 rb s3://{} --force

# 5. Supprimer TOUTES les fonctions Lambda
for region in us-east-2 us-east-1; do
  aws lambda list-functions --region $region --query 'Functions[*].FunctionName' --output text | xargs -I {} aws lambda delete-function --region $region --function-name {}
done
```

## Ce qui a causé le passage au forfait payant

1. **AWS Organizations**: Service réservé aux entreprises, sort du Free Tier
2. **Création de comptes multiples**: Chaque compte peut générer des frais

## Recommandation finale

**Pour ce projet académique, je recommande:**

1. ✅ Faire le TD6 Partie 2 et 3 SANS multi-comptes AWS
2. ✅ Utiliser Kubernetes LOCAL (Docker Desktop)
3. ✅ Documenter théoriquement la Partie 1 sans l'implémenter
4. ✅ Surveiller votre facture AWS QUOTIDIENNEMENT
5. ✅ Détruire IMMÉDIATEMENT toute ressource après les tests

**RÈGLE D'OR**: Si vous voyez des frais, même minimes, ARRÊTEZ et nettoyez TOUT!

---

## Contact AWS Support

Si vous voulez vraiment revenir au Free Tier ou fermer les comptes Organizations:
- AWS Support Center: https://console.aws.amazon.com/support/home
- Demandez la fermeture immédiate des comptes child (stage, prod)
- Expliquez que c'est un projet académique

## Coût estimé actuel

- Comptes Organizations créés: ~$0/mois (si vides)
- MAIS attention à la fermeture qui prend 90 jours

**Total dépensé jusqu'ici**: Probablement $0 (tout a été détruit rapidement)
