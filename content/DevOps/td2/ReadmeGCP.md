# 🚀 Déploiement d'une Application Node.js sur Google Cloud Platform (GCP)

> **Guide Complet pour Débutants - De Zéro à Production sur GCP**
>
> Par **samba-diallo** | Octobre 2025

[![GCP](https://img.shields.io/badge/Google_Cloud-Compute_Engine-blue?style=flat&logo=google-cloud)](https://cloud.google.com/)
[![Node.js](https://img.shields.io/badge/Node.js-21.x-green?style=flat&logo=node.js)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DevOps](https://img.shields.io/badge/DevOps-Basics-blueviolet)](https://cloud.google.com/)

---

## 📑 Table des Matières

- [Introduction](#-introduction)
- [Prérequis](#-prérequis)
- [Partie 1 : Configuration GCP](#-partie-1--configuration-gcp)
- [Partie 2 : Déploiement Compute Engine](#-partie-2--déploiement-compute-engine)
- [Partie 3 : Comprendre le Code](#-partie-3--comprendre-le-code)
- [Partie 4 : Test & Vérification](#-partie-4--test--vérification)
- [Exercices Pratiques](#-exercices-pratiques)
- [Dépannage](#-dépannage)
- [Nettoyage](#-nettoyage)
- [GCP vs AWS : Comparaison](#-gcp-vs-aws--comparaison)
- [Conclusion](#-conclusion)
- [Ressources](#-ressources)

---

## 🎯 Introduction

### Qu'allez-vous Apprendre ?

Ce guide vous apprend à déployer une application web simple sur **Google Cloud Platform (GCP)** en utilisant **Compute Engine** (équivalent d'EC2 sur AWS). Vous découvrirez l'écosystème Google Cloud et comparerez avec AWS.

### 🎓 Compétences Acquises

- ✅ Créer et configurer un compte Google Cloud
- ✅ Gérer les identités avec IAM (Identity and Access Management)
- ✅ Lancer une VM (Virtual Machine) sur Compute Engine
- ✅ Configurer des règles de pare-feu (Firewall Rules)
- ✅ Automatiser avec Startup Scripts
- ✅ Déployer une application Node.js sur GCP
- ✅ Comparer GCP et AWS

### 💼 Pourquoi Google Cloud Platform ?

```
🌐 GCP dans le Monde
   → #3 mondial du cloud (10% de parts de marché)
   → Utilisé par : Spotify, Twitter, Snapchat, PayPal
   → Infrastructure de Google (Gmail, YouTube, Search)

💡 Avantages Uniques de GCP
   → Réseau privé global le plus rapide
   → Pricing transparent et prévisible
   → Live migration (maintenance sans downtime)
   → BigQuery (analytics à l'échelle mondiale)
   → Kubernetes natif (GKE - Google Kubernetes Engine)

💰 Opportunités Carrière
   → Cloud Engineer (GCP) : 65-110k€/an
   → Data Engineer (GCP) : 70-120k€/an
   → Compétence complémentaire à AWS

🔄 Comparaison avec AWS
   → GCP : Simplicité, innovation, data analytics
   → AWS : Maturité, breadth de services, market leader
   → Multi-cloud = Valeur ajoutée sur le marché
```

---

## 📋 Prérequis

### Connaissances

| Niveau | Requis |
|--------|--------|
| **Essentiel** | Utilisation d'un navigateur web |
| **Recommandé** | Notions de ligne de commande (bash/shell) |
| **Utile** | Bases de JavaScript/Node.js |
| **Bonus** | Connaissance d'AWS (pour comparaison) |

### Outils Nécessaires

| Outil | Utilité | Téléchargement |
|-------|---------|----------------|
| **Navigateur Web** | Accès GCP Console | Chrome (recommandé), Firefox |
| **Compte Google** | Authentification | [Gmail](https://gmail.com) |
| **Carte Bancaire** | Vérification (300$ gratuits) | - |

### 💰 Coûts GCP

```
✅ GCP Free Tier (Toujours gratuit)
   → e2-micro VM : 1 instance/mois GRATUIT (US regions)
   → 30 GB stockage persistant
   → 5 GB snapshots
   → 1 GB réseau sortant/mois

🎁 GCP Free Trial (Nouvel utilisateur)
   → 300 USD de crédits GRATUITS
   → Valable 90 jours
   → Aucune facturation automatique après expiration
   → Carte bancaire requise (vérification, pas de débit)

💡 Pour ce Tutoriel
   → Coût : 0€ (avec Free Trial)
   → VM e2-micro (Always Free Tier)
   → Durée : ~2-3 heures de test
   → N'oubliez pas de supprimer après !

⚠️ Important
   → Utilisez e2-micro (Always Free)
   → Région : us-central1, us-west1, ou us-east1
   → Supprimez les ressources après test
```

---

## 🔐 Partie 1 : Configuration GCP

### Étape 1.1 : Créer un Compte Google Cloud

#### 🔗 Inscription

**1. Accéder à GCP**

```
https://cloud.google.com
```

**2. Cliquer sur "Get started for free" (Commencer gratuitement)**

**3. Se Connecter avec Compte Google**

```
Utilisez un compte Gmail existant
OU
Créez un nouveau compte Google
```

**4. Accepter les Conditions d'Utilisation**

```
☑️ Terms of Service
☑️ Email updates (optionnel)
```

**5. Informations de Compte**

| Information | Exemple | Requis |
|-------------|---------|--------|
| **Pays** | France | ✅ |
| **Type de compte** | Individual (Particulier) | ✅ |
| **Carte bancaire** | VISA/MasterCard | ✅ (vérification) |

**6. Vérification de la Carte**

```
Prélèvement : 0€ ou ~1€ (remboursé immédiatement)
But : Vérification que vous n'êtes pas un robot
⚠️ Aucune facturation automatique après Free Trial
```

**7. Confirmation**

```
✅ 300 USD de crédits ajoutés
✅ Valables 90 jours
✅ Compte GCP créé !
```

---

#### 🎨 Interface GCP Console

**Accéder à la Console :**

```
https://console.cloud.google.com
```

**Éléments Clés :**

| Élément | Description | Emplacement |
|---------|-------------|-------------|
| **Navigation Menu** | ☰ Tous les services GCP | Haut gauche |
| **Project Selector** | Choisir/créer un projet | Haut (nom du projet) |
| **Search Bar** | Rechercher services/ressources | Haut centre |
| **Cloud Shell** | Terminal dans le navigateur | Icône `>_` en haut |
| **Notifications** | Alertes et logs | Icône cloche |

---

### Étape 1.2 : Créer un Projet GCP

#### 🎯 Qu'est-ce qu'un Projet GCP ?

```
Projet GCP = Conteneur logique pour vos ressources

Caractéristiques :
→ Isole les ressources (VMs, databases, etc.)
→ Facturation séparée
→ Permissions granulaires (IAM)
→ Quotas et limites indépendants

Analogie :
→ Projet = Dossier pour organiser vos fichiers
→ Ressources = Fichiers dans le dossier

Bonnes Pratiques :
→ 1 projet par environnement (dev, staging, prod)
→ 1 projet par application
→ Nommage cohérent (ex : mon-app-dev)
```

---

#### 📝 Création du Projet

**Méthode 1 : Via l'Interface**

```
1. Cliquer sur le sélecteur de projet (haut de la page)
2. Cliquer sur "NEW PROJECT" (Nouveau projet)
3. Remplir les informations
```

**Configuration :**

| Champ | Valeur | Exemple |
|-------|--------|---------|
| **Project name** | Nom descriptif | `sample-app-project` |
| **Project ID** | Identifiant unique (généré auto) | `sample-app-project-438201` |
| **Organization** | Laisser vide (pas d'organisation) | - |
| **Location** | No organization | - |

**4. Cliquer sur "CREATE"**

**5. Confirmation**

```
✅ Projet créé !
🔄 Basculer vers le nouveau projet (sélecteur en haut)
```

---

**Méthode 2 : Via Cloud Shell (Avancé)**

```bash
# Ouvrir Cloud Shell (icône >_ en haut)

# Créer un projet
gcloud projects create sample-app-project-$RANDOM \
    --name="Sample App Project"

# Définir comme projet par défaut
gcloud config set project sample-app-project-XXXXX

# Vérifier
gcloud config get-value project
```

---

#### ⚙️ Activer les APIs Nécessaires

**GCP nécessite d'activer les APIs avant utilisation**

**APIs à Activer :**

```
1. Compute Engine API
2. Cloud Resource Manager API (déjà activée)
```

**Activation via Interface :**

```
1. Navigation Menu (☰)
2. APIs & Services → Library
3. Rechercher : "Compute Engine API"
4. Cliquer dessus
5. Bouton "ENABLE" (Activer)
6. Attendre ~30 secondes
```

**Activation via Cloud Shell :**

```bash
# Activer Compute Engine API
gcloud services enable compute.googleapis.com

# Vérifier les APIs activées
gcloud services list --enabled
```

---

### Étape 1.3 : Configuration IAM (Identity and Access Management)

#### 🎯 Comprendre IAM sur GCP

**IAM = Who can do What on Which resource**

```
Concepts Clés :

1. Members (Qui)
   → Google Account (user@gmail.com)
   → Service Account (app@project.iam.gserviceaccount.com)
   → Google Group
   → Cloud Identity domain

2. Roles (Quoi)
   → Primitive : Owner, Editor, Viewer
   → Predefined : roles/compute.admin
   → Custom : Créés par vous

3. Resources (Sur quoi)
   → Project
   → VM instance
   → Storage bucket
   → Etc.

Modèle :
Member + Role → Access to Resource
```

---

#### 🔐 Créer un Compte de Service (Service Account)

**Qu'est-ce qu'un Service Account ?**

```
Service Account = Identité pour applications/VMs

Différence User vs Service Account :

User Account :
→ Pour humains (vous)
→ Connexion via Google login
→ MFA, récupération de compte

Service Account :
→ Pour applications/scripts
→ Authentification via clés
→ Pas d'interface utilisateur

Usage :
→ VM qui accède à Cloud Storage
→ Application qui écrit dans BigQuery
→ Script qui crée des ressources
```

---

**Création :**

**Via Interface :**

```
1. Navigation Menu (☰)
2. IAM & Admin → Service Accounts
3. "+ CREATE SERVICE ACCOUNT"
4. Configuration :
```

| Champ | Valeur |
|-------|--------|
| **Service account name** | `sample-app-sa` |
| **Service account ID** | `sample-app-sa` (auto-généré) |
| **Description** | `Service account for sample app` |

```
5. CONTINUE
6. Grant this service account access to project :
   Role : Compute Admin (roles/compute.admin)
7. CONTINUE
8. DONE
```

**Via Cloud Shell :**

```bash
# Créer service account
gcloud iam service-accounts create sample-app-sa \
    --display-name="Sample App Service Account"

# Ajouter le rôle
PROJECT_ID=$(gcloud config get-value project)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:sample-app-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/compute.admin"
```

---

#### 🛡️ Activer l'Authentification à Deux Facteurs (2FA)

**Pour votre Compte Google :**

```
1. Aller sur : https://myaccount.google.com/security
2. Section "Signing in to Google"
3. Cliquer sur "2-Step Verification"
4. Suivre les instructions :
   - Numéro de téléphone (SMS)
   OU
   - Google Authenticator (recommandé)
5. Activer
```

**Pourquoi c'est CRITIQUE :**

```
Statistiques Sécurité :
→ 2FA bloque 100% des bots automatisés (Google)
→ 99% des attaques de phishing (Microsoft)
→ Protection compte Google = Protection GCP

⚠️ Sans 2FA :
❌ Compte Google compromis = Accès GCP
❌ Peut générer des milliers d'euros de factures
❌ Peut supprimer toutes vos données

✅ Avec 2FA :
✅ Protection maximale
✅ Standard entreprise
✅ Obligation pour comptes critiques
```

---

### Étape 1.4 : Configuration de la Facturation

#### 💳 Comprendre la Facturation GCP

**Modèle de Facturation :**

```
GCP Billing = Pay-as-you-go

Concepts :
→ Billing Account (Compte de facturation)
→ Projects liés au compte
→ Budgets et alertes
→ Free Tier toujours actif

Transparence :
→ Pricing Calculator
→ Facturation à la seconde (vs minute sur AWS)
→ Sustained Use Discounts (réductions automatiques)
→ Committed Use Discounts (contrats long terme)
```

---

**Vérifier le Compte de Facturation :**

```
1. Navigation Menu (☰)
2. Billing
3. Vous devriez voir :
   - My Billing Account
   - Free trial status : $300 remaining
   - Days remaining : ~90
```

**Configurer un Budget (Recommandé) :**

```
1. Billing → Budgets & alerts
2. CREATE BUDGET
3. Configuration :
```

| Paramètre | Valeur |
|-----------|--------|
| **Name** | `Sample App Budget` |
| **Projects** | Sélectionner votre projet |
| **Budget amount** | `10 USD` |
| **Alert threshold** | `50%, 90%, 100%` |
| **Email notifications** | Votre email |

```
4. FINISH
```

**Résultat :**

```
✅ Email si dépenses > 5 USD (50%)
✅ Email si dépenses > 9 USD (90%)
✅ Email si dépenses > 10 USD (100%)
⚠️ Budget = Alerte seulement (pas de coupure automatique)
```

---

## 🖥️ Partie 2 : Déploiement Compute Engine

### Qu'est-ce que Compute Engine ?

**Compute Engine = Service de VMs (Virtual Machines) de GCP**

```
Définition :
→ Équivalent d'EC2 sur AWS
→ Serveurs virtuels à la demande
→ Infrastructure Google mondiale

Avantages :
✅ Démarrage ultra-rapide (~20 secondes)
✅ Live migration (maintenance sans interruption)
✅ Réseau privé Google (latence minimale)
✅ Disques persistants haute performance
✅ Snapshots et backups automatiques

Cas d'usage :
→ Héberger applications web
→ Serveurs de base de données
→ Calcul haute performance
→ Containers (avant Kubernetes)
→ CI/CD runners
```

---

### Étape 2.1 : Lancer une Instance VM

#### 🚀 Accéder à Compute Engine

**Via Interface :**

```
1. Navigation Menu (☰)
2. Compute Engine → VM instances
3. Si première utilisation :
   - Attendre initialisation (~1 minute)
   - API Compute Engine s'active
4. Cliquer "CREATE INSTANCE"
```

---

#### 📝 Configuration de l'Instance

**1️⃣ Nom et Région**

| Paramètre | Valeur | Explication |
|-----------|--------|-------------|
| **Name** | `sample-app-vm` | Identifiant de la VM |
| **Labels** | `env=dev`, `app=sample` | Organisation (optionnel) |
| **Region** | `us-central1` | Iowa, USA (Free Tier) |
| **Zone** | `us-central1-a` | Zone de disponibilité |

**Pourquoi us-central1 ?**

```
Free Tier (Always Free) :
→ us-west1 (Oregon)
→ us-central1 (Iowa)
→ us-east1 (South Carolina)

Autres régions = Facturation normale

Pour ce tutoriel :
✅ Choisir us-central1 (Free Tier)
❌ europe-west1 (Belgique) = Coût
```

---

**2️⃣ Machine Configuration (Type de VM)**

**GCP propose plusieurs familles de machines :**

| Famille | Usage | Exemple |
|---------|-------|---------|
| **E2** | Usage général, économique | e2-micro, e2-small |
| **N2** | Balanced, haute performance | n2-standard-2 |
| **C2** | Compute-optimized | c2-standard-4 |
| **M2** | Memory-optimized | m2-ultramem-208 |

**Configuration pour ce Tutoriel :**

```
☑️ Machine family : General-purpose
☑️ Series : E2
☑️ Machine type : e2-micro

Specs :
- 2 vCPUs (shared-core)
- 1 GB RAM
- ✅ FREE TIER (Always Free)

Coût (si hors Free Tier) :
- ~$6.11/mois (730 heures)
- ~$0.008365/heure
```

**Comparaison Types de Machines :**

| Type | vCPU | RAM | Coût/mois | Free Tier |
|------|------|-----|-----------|-----------|
| **e2-micro** | 2 | 1 GB | $6.11 | ✅ |
| e2-small | 2 | 2 GB | $12.22 | ❌ |
| e2-medium | 2 | 4 GB | $24.44 | ❌ |
| e2-standard-2 | 2 | 8 GB | $48.88 | ❌ |

---

**3️⃣ Boot Disk (Disque de Démarrage)**

**Cliquer sur "CHANGE" (Modifier)**

| Paramètre | Valeur |
|-----------|--------|
| **Operating System** | Ubuntu |
| **Version** | Ubuntu 22.04 LTS (Jammy Jellyfish) |
| **Boot disk type** | Standard persistent disk |
| **Size** | 10 GB |

**Pourquoi Ubuntu ?**

```
Ubuntu 22.04 LTS :
✅ Long Term Support (5 ans de mises à jour)
✅ Large communauté
✅ APT package manager (familier)
✅ Compatible avec la plupart des tutos
✅ Support Docker natif

Alternatives :
- Debian 11 (plus léger)
- CentOS Stream (Red Hat ecosystem)
- Container-Optimized OS (pour containers)
```

**Cliquer "SELECT" (Sélectionner)**

---

**4️⃣ Firewall (Pare-feu)** 🔥 CRITIQUE

**Dans la section "Firewall" :**

```
☑️ Allow HTTP traffic
☐ Allow HTTPS traffic (pas nécessaire pour ce tuto)
```

**⚠️ IMPORTANT :**

```
Cocher "Allow HTTP traffic" :
→ Crée automatiquement une règle de firewall
→ Autorise le port 80 (HTTP)
→ Source : 0.0.0.0/0 (tout Internet)

Sans cette option :
❌ Firewall bloque tout le trafic HTTP
❌ Erreur "Connection timeout"
❌ Application inaccessible
```

---

**5️⃣ Management, Security, Disks, Networking, Sole Tenancy**

**Cliquer sur "Management" pour développer**

**Naviguer vers "Automation" (en bas de Management)**

**Section "Startup script" :**

C'est ici que nous allons coller notre script d'installation !

---

### Étape 2.2 : Le Startup Script

#### 🎯 Qu'est-ce qu'un Startup Script ?

```
Startup Script = Script exécuté au démarrage de la VM

Équivalent :
→ AWS : User Data
→ GCP : Startup Script / Metadata

Caractéristiques :
✅ Exécuté automatiquement par GCP
✅ À chaque démarrage (différence avec AWS !)
✅ Privilèges root
✅ Permet automation

Différence AWS vs GCP :
AWS User Data → 1 seule fois (premier boot)
GCP Startup Script → À chaque boot (par défaut)

Configuration :
→ Stocké dans instance metadata
→ Peut être mis à jour sans recréer la VM
```

---

#### 📝 Le Script Complet

**Copier-coller dans "Startup script" :**

```bash
#!/bin/bash
set -e

# Log everything
exec > >(tee /var/log/startup-script.log)
exec 2>&1

echo "=========================================="
echo "Starting Startup Script"
echo "Time: $(date)"
echo "=========================================="

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Node.js 21.x
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_21.x | bash -
apt-get install -y nodejs

# Verify installation
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Create application directory
echo "Creating application directory..."
mkdir -p /opt/sample-app
cd /opt/sample-app

# Create app.js
echo "Creating app.js..."
cat > /opt/sample-app/app.js << 'EOF'
const http = require('http');
const os = require('os');

const server = http.createServer((req, res) => {
  const hostname = os.hostname();
  const platform = os.platform();
  const uptime = process.uptime();
  
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Hello from GCP!</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          max-width: 800px;
          margin: 50px auto;
          padding: 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }
        .container {
          background: rgba(255,255,255,0.1);
          padding: 30px;
          border-radius: 10px;
          backdrop-filter: blur(10px);
        }
        h1 { margin-top: 0; }
        .info { margin: 10px 0; }
        code {
          background: rgba(0,0,0,0.3);
          padding: 2px 6px;
          border-radius: 3px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🎉 Hello from Google Cloud Platform!</h1>
        <p class="info">✅ Your Node.js app is running successfully on GCP Compute Engine</p>
        <hr>
        <p class="info"><strong>Hostname:</strong> <code>${hostname}</code></p>
        <p class="info"><strong>Platform:</strong> <code>${platform}</code></p>
        <p class="info"><strong>App Uptime:</strong> <code>${uptime.toFixed(2)}s</code></p>
        <p class="info"><strong>Node.js:</strong> <code>${process.version}</code></p>
        <hr>
        <p style="font-size: 12px; opacity: 0.8;">
          Deployed by: samba-diallo | Tutorial: GCP Compute Engine Deployment
        </p>
      </div>
    </body>
    </html>
  `);
});

const port = process.env.PORT || 80;
server.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log(`Hostname: ${os.hostname()}`);
});
EOF

# Install PM2 for process management
echo "Installing PM2..."
npm install -g pm2

# Start application with PM2
echo "Starting application with PM2..."
pm2 start /opt/sample-app/app.js --name sample-app

# Configure PM2 to start on boot
echo "Configuring PM2 startup..."
pm2 startup systemd -u root --hp /root
pm2 save

echo "=========================================="
echo "Startup Script Completed Successfully!"
echo "Time: $(date)"
echo "=========================================="
```

---

### Étape 2.3 : Explication Détaillée du Script

#### Partie 1 : Initialisation et Logging

```bash
#!/bin/bash
set -e

# Log everything
exec > >(tee /var/log/startup-script.log)
exec 2>&1

echo "Starting Startup Script"
echo "Time: $(date)"
```

**Explication :**

| Ligne | Signification |
|-------|---------------|
| `#!/bin/bash` | Exécute avec Bash |
| `set -e` | Arrête si erreur |
| `exec > >(tee ...)` | Redirige sortie vers fichier + écran |
| `exec 2>&1` | Redirige erreurs vers sortie standard |

**Résultat :**

```
✅ Tous les logs sauvegardés dans /var/log/startup-script.log
✅ Visible dans console GCP (Cloud Logging)
✅ Facilite le débogage
```

---

#### Partie 2 : Mise à Jour Système

```bash
echo "Updating system packages..."
apt-get update
apt-get upgrade -y
```

**Pourquoi ?**

```
Sécurité :
→ Patches de sécurité récents
→ Corrections de bugs
→ Dernières versions des packages

Bonnes pratiques :
✅ Toujours mettre à jour avant install
✅ Évite les conflits de dépendances
```

---

#### Partie 3 : Installation Node.js

```bash
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_21.x | bash -
apt-get install -y nodejs

echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"
```

**Différence avec AWS :**

| Aspect | AWS (Amazon Linux) | GCP (Ubuntu) |
|--------|-------------------|--------------|
| Gestionnaire | `yum` | `apt-get` |
| Repo Node.js | `rpm.nodesource.com` | `deb.nodesource.com` |
| Format packages | `.rpm` | `.deb` |

---

#### Partie 4 : Création de l'Application

```bash
mkdir -p /opt/sample-app
cd /opt/sample-app

cat > /opt/sample-app/app.js << 'EOF'
const http = require('http');
const os = require('os');

const server = http.createServer((req, res) => {
  const hostname = os.hostname();
  const platform = os.platform();
  const uptime = process.uptime();
  
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`
    <!DOCTYPE html>
    <html>
    ...
  `);
});

const port = process.env.PORT || 80;
server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
EOF
```

**Améliorations par rapport à AWS :**

```
✅ HTML formaté (plus joli qu'un simple texte)
✅ Affiche des infos système (hostname, uptime)
✅ CSS intégré (gradient background)
✅ Plus professionnel

Modules utilisés :
→ http : Serveur HTTP
→ os : Informations système
```

---

#### Partie 5 : PM2 Process Manager 🚀 NOUVEAU !

```bash
npm install -g pm2

pm2 start /opt/sample-app/app.js --name sample-app

pm2 startup systemd -u root --hp /root
pm2 save
```

**Qu'est-ce que PM2 ?**

```
PM2 = Production Process Manager for Node.js

Avantages :
✅ Redémarre l'app si crash
✅ Démarre automatiquement au boot
✅ Load balancing (plusieurs instances)
✅ Logs centralisés
✅ Monitoring intégré
✅ Zero-downtime reload

Différence avec AWS :
AWS User Data → "nohup node app.js &" (basique)
GCP Startup Script → PM2 (production-ready)
```

**Commandes PM2 :**

| Commande | Action |
|----------|--------|
| `pm2 start app.js` | Démarre l'app |
| `pm2 stop app` | Arrête l'app |
| `pm2 restart app` | Redémarre l'app |
| `pm2 logs` | Voir les logs |
| `pm2 list` | Lister les apps |
| `pm2 monit` | Monitoring temps réel |
| `pm2 save` | Sauvegarder la config |

---

### Étape 2.4 : Lancement de l'Instance

**Actions Finales :**

```
1. ✅ Vérifier tous les paramètres :
   - Name : sample-app-vm
   - Region : us-central1
   - Machine type : e2-micro
   - Boot disk : Ubuntu 22.04 LTS
   - Firewall : HTTP autorisé
   - Startup script : Collé

2. ✅ Faire défiler en bas de la page

3. 🚀 Cliquer sur "CREATE" (bouton bleu)
```

---

**Timeline de Création :**

```
00:00 - Clic sur CREATE
00:05 - GCP alloue les ressources
00:10 - VM démarre (boot Ubuntu)
00:20 - État : RUNNING ✅
00:30 - Startup Script commence
01:00 - Installation Node.js
01:30 - Installation PM2
02:00 - Application démarrée
02:30 - Prêt à tester ! ✅
```

**Temps total : ~2-3 minutes**

---

**Page de Résultat :**

```
✅ Message : "Instance created"
```

**Informations Visibles :**

| Information | Exemple | Utilité |
|-------------|---------|---------|
| **Name** | sample-app-vm | Identifiant |
| **Zone** | us-central1-a | Localisation |
| **Internal IP** | 10.128.0.2 | Réseau interne GCP |
| **External IP** | 34.122.45.67 | Accès Internet |
| **Status** | RUNNING | État |

---

## 💻 Partie 3 : Comprendre le Code

### Architecture de l'Application sur GCP

```
┌─────────────────────────────────┐
│    Internet (Clients)           │
└────────────┬────────────────────┘
             │ HTTP Request
             ↓
┌────────────────────────────────────┐
│  GCP VPC Firewall Rules            │
│  default-allow-http (tag: http)    │
│  Ports: 80                         │
└────────────┬───────────────────────┘
             │ Traffic autorisé
             ↓
┌────────────────────────────────────┐
│  Compute Engine VM                 │
│  Region: us-central1               │
│  Zone: us-central1-a               │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Ubuntu 22.04 LTS            │  │
│  │  ┌────────────────────────┐  │  │
│  │  │  Node.js 21.x          │  │  │
│  │  │  ┌──────────────────┐  │  │  │
│  │  │  │  PM2 Manager     │  │  │  │
│  │  │  │  ┌────────────┐  │  │  │  │
│  │  │  │  │  app.js    │  │  │  │  │
│  │  │  │  │  Port 80   │  │  │  │  │
│  │  │  │  └────────────┘  │  │  │  │
│  │  │  └──────────────────┘  │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
│                                    │
│  Logs → Cloud Logging              │
└────────────┬───────────────────────┘
             │ HTTP Response
             │ HTML + CSS
             ↓
┌────────────────────────────────────┐
│   Navigateur (Client)              │
│   Affiche page stylisée            │
└────────────────────────────────────┘
```

---

### Code Node.js Expliqué

#### Import des Modules

```javascript
const http = require('http');
const os = require('os');
```

**Module `os` (Operating System) :**

```javascript
os.hostname()  // Nom de la machine (ex: sample-app-vm)
os.platform()  // Système d'exploitation (ex: linux)
os.uptime()    // Temps depuis démarrage OS
os.cpus()      // Informations CPUs
os.totalmem()  // RAM totale
os.freemem()   // RAM disponible
```

---

#### Création du Serveur avec Infos Système

```javascript
const server = http.createServer((req, res) => {
  const hostname = os.hostname();
  const platform = os.platform();
  const uptime = process.uptime();
  
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`...HTML...`);
});
```

**Différences avec version AWS :**

| Aspect | AWS Version | GCP Version |
|--------|-------------|-------------|
| Content-Type | `text/plain` | `text/html` |
| Corps | `Hello, World!\n` | Page HTML complète |
| Infos | Aucune | Hostname, Platform, Uptime |
| Styling | Non | CSS avec gradient |
| Professionalisme | Basique | Production-ready |

---

#### Template Literals Avancés

```javascript
res.end(`
  <!DOCTYPE html>
  <html>
  <head>
    <title>Hello from GCP!</title>
    <style>
      body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
    </style>
  </head>
  <body>
    <h1>Hello from Google Cloud Platform!</h1>
    <p>Hostname: <code>${hostname}</code></p>
    <p>Uptime: <code>${uptime.toFixed(2)}s</code></p>
  </body>
  </html>
`);
```

**Fonctionnalités :**

```
Template Literals :
→ Backticks `...` (pas quotes '...')
→ Multiligne sans concaténation
→ Interpolation ${variable}
→ Expressions ${expr.method()}

CSS Inline :
→ Linear gradient background
→ Responsive (max-width)
→ Glass morphism effect (backdrop-filter)
→ Professional look
```

---

### Gestion de Processus avec PM2

#### Pourquoi PM2 est Crucial

**Sans PM2 (approche AWS basique) :**

```
Problèmes :
❌ App crash → Downtime complet
❌ Redémarrage VM → App ne redémarre pas
❌ Pas de logs persistants
❌ Pas de monitoring
❌ Pas de load balancing

Exemple de crash :
→ Exception non gérée
→ Mémoire insuffisante
→ Bug dans le code
→ App s'arrête → Site down ❌
```

**Avec PM2 (approche GCP de ce tuto) :**

```
Avantages :
✅ Crash → Redémarrage automatique (0.1s)
✅ Redémarrage VM → App redémarre auto
✅ Logs sauvegardés dans /root/.pm2/logs/
✅ Monitoring : pm2 monit
✅ Cluster mode : pm2 start -i max (multi-CPU)

Exemple de crash :
→ Exception non gérée
→ PM2 détecte le crash
→ Redémarre l'app en 100ms
→ Site reste up ✅
```

---

#### Cycle de Vie d'une App avec PM2

```
1. Démarrage
   pm2 start app.js
   ↓
2. App Running
   PM2 surveille le processus
   ↓
3. Crash détecté
   App s'est arrêtée
   ↓
4. Redémarrage Auto
   PM2 relance l'app (< 1s)
   ↓
5. Back to Running
   App disponible à nouveau

VM Reboot :
1. Systemd démarre
2. Systemd lance PM2
3. PM2 lit la config sauvegardée
4. PM2 relance toutes les apps
5. Apps disponibles ✅
```

---

#### Commandes PM2 Utiles

**Gestion de Base :**

```bash
# Lister les applications
pm2 list

# Voir les logs en temps réel
pm2 logs

# Logs d'une app spécifique
pm2 logs sample-app

# Monitoring en temps réel
pm2 monit

# Redémarrer une app
pm2 restart sample-app

# Arrêter une app
pm2 stop sample-app

# Supprimer une app de PM2
pm2 delete sample-app
```

**Cluster Mode (Load Balancing) :**

```bash
# Démarrer en mode cluster (autant d'instances que de CPUs)
pm2 start app.js -i max

# Ou nombre spécifique
pm2 start app.js -i 4

# Recharger sans downtime
pm2 reload sample-app
```

**Configuration Avancée :**

```bash
# Créer fichier ecosystem.config.js
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'sample-app',
    script: '/opt/sample-app/app.js',
    instances: 2,
    exec_mode: 'cluster',
    watch: true,
    max_memory_restart: '300M',
    env: {
      NODE_ENV: 'production',
      PORT: 80
    }
  }]
};
EOF

# Démarrer avec config
pm2 start ecosystem.config.js
```

---

### Comparaison : Startup Script vs User Data

| Aspect | GCP Startup Script | AWS User Data |
|--------|-------------------|---------------|
| **Exécution** | À chaque boot | Premier boot uniquement |
| **Stockage** | Instance metadata | Instance metadata |
| **Modification** | Possible sans recréer VM | Nécessite recréer instance |
| **Logs** | Cloud Logging auto | Nécessite config |
| **Taille max** | 256 KB | 16 KB |
| **Format** | Bash, Python, etc. | Bash, PowerShell |

---

## ✅ Partie 4 : Test & Vérification

### Étape 4.1 : Observer le Démarrage

#### Page VM Instances

```
Compute Engine → VM instances
```

**Vous devriez voir :**

| Colonne | Valeur | Signification |
|---------|--------|---------------|
| **Name** | sample-app-vm | Votre VM |
| **Zone** | us-central1-a | Localisation |
| **Internal IP** | 10.128.0.2 | IP privée GCP |
| **External IP** | 34.122.45.67 | IP publique Internet |
| **Connect** | SSH | Bouton de connexion |

---

#### États de la VM

```
Progression :
⏳ PROVISIONING → Allocation des ressources
⏳ STAGING → Préparation
🟢 RUNNING → VM active ✅

Autres états possibles :
🔴 STOPPING → En arrêt
⏹️ TERMINATED → Arrêtée
🔄 SUSPENDING → Suspension en cours
```

---

### Étape 4.2 : Récupérer l'IP Publique

**Option 1 : Via l'Interface**

```
VM instances → Colonne "External IP"
Exemple : 34.122.45.67
```

**Option 2 : Via Cloud Shell**

```bash
# Ouvrir Cloud Shell (icône >_ en haut)

# Lister les instances
gcloud compute instances list

# Obtenir l'IP externe
gcloud compute instances describe sample-app-vm \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

---

### Étape 4.3 : Vérifier les Logs de Démarrage

**Via l'Interface :**

```
1. VM instances
2. Cliquer sur "sample-app-vm"
3. Onglet "Logs" (ou "OBSERVABILITY" → "Logs")
4. Chercher : "startup-script"
```

**Vous devriez voir :**

```
Starting Startup Script
Updating system packages...
Installing Node.js...
Node.js version: v21.x.x
Installing PM2...
Starting application with PM2...
Startup Script Completed Successfully!
```

---

**Via Cloud Shell (SSH) :**

```bash
# Se connecter à la VM
gcloud compute ssh sample-app-vm --zone=us-central1-a

# Voir les logs du startup script
sudo cat /var/log/startup-script.log

# Vérifier le statut PM2
sudo pm2 list

# Voir les logs de l'app
sudo pm2 logs sample-app

# Quitter SSH
exit
```

---

### Étape 4.4 : Tester l'Application

#### Dans votre Navigateur

```
1. Copier l'IP externe : 34.122.45.67
2. Ouvrir navigateur
3. Taper : http://34.122.45.67
   
⚠️ Important : http:// (pas https://)

4. Appuyer sur Entrée
```

---

#### 🎉 Résultat Attendu

**Vous devriez voir une page stylisée avec :**

```
🎉 Hello from Google Cloud Platform!

✅ Your Node.js app is running successfully on GCP Compute Engine

────────────────────────────────────

Hostname: sample-app-vm
Platform: linux
App Uptime: 123.45s
Node.js: v21.x.x

────────────────────────────────────

Deployed by: samba-diallo | Tutorial: GCP Compute Engine Deployment
```

**Design :**

```
✅ Fond avec gradient violet/bleu
✅ Conteneur avec effet glass morphism
✅ Informations système dynamiques
✅ Aspect professionnel
```

---

**FÉLICITATIONS !** 🎊

```
✅ Application déployée sur GCP !
✅ VM accessible sur Internet
✅ PM2 gère votre app
✅ Logs centralisés
✅ Production-ready setup !
```

---

### Étape 4.5 : Tests Avancés

#### Test 1 : Rafraîchissement Multiple

```
Action :
→ Appuyer sur F5 plusieurs fois dans le navigateur

Observation :
→ "App Uptime" augmente à chaque refresh
→ Hostname reste le même
→ Réponse rapide (< 100ms)

Conclusion :
✅ App stable
✅ PM2 maintient le processus
✅ Pas de restart intempestif
```

---

#### Test 2 : Vérifier PM2 Status

```bash
# SSH dans la VM
gcloud compute ssh sample-app-vm --zone=us-central1-a

# Statut PM2
sudo pm2 status

# Résultat attendu :
┌─────┬──────────────┬─────────────┬─────────┬─────────┬──────────┐
│ id  │ name         │ mode        │ ↺       │ status  │ cpu      │
├─────┼──────────────┼─────────────┼─────────┼─────────┼──────────┤
│ 0   │ sample-app   │ fork        │ 0       │ online  │ 0%       │
└─────┴──────────────┴─────────────┴─────────┴─────────┴──────────┘

# Monitoring temps réel
sudo pm2 monit

# Quitter : Ctrl+C puis exit
```

---

#### Test 3 : Vérifier les Règles de Firewall

**Via Interface :**

```
1. Navigation Menu (☰)
2. VPC network → Firewall
3. Chercher : "default-allow-http"
4. Vérifier :
```

| Paramètre | Valeur |
|-----------|--------|
| **Targets** | Specified target tags: http-server |
| **Source filter** | IP ranges: 0.0.0.0/0 |
| **Protocols / ports** | tcp:80 |
| **Action on match** | Allow |

**Via Cloud Shell :**

```bash
gcloud compute firewall-rules list --filter="name:default-allow-http"
```

---

## 🏋️ Exercices Pratiques

### Exercice 1 : Test de Crash Recovery

#### Objectif

Démontrer la résilience de PM2 en cas de crash applicatif.

---

#### Actions

**1. Se Connecter à la VM**

```bash
gcloud compute ssh sample-app-vm --zone=us-central1-a
```

**2. Modifier l'App pour Crasher**

```bash
# Créer une version qui crash
sudo cat > /opt/sample-app/crash-app.js << 'EOF'
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/crash') {
    // Crash intentionnel
    throw new Error('Intentional crash!');
  }
  
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello! Visit /crash to crash the app\n');
});

server.listen(80, () => {
  console.log('Crash test server running on port 80');
});
EOF

# Remplacer l'app par la version crash
sudo pm2 stop sample-app
sudo pm2 delete sample-app
sudo pm2 start /opt/sample-app/crash-app.js --name sample-app
sudo pm2 save
```

**3. Tester le Crash**

```bash
# Dans la VM
curl http://localhost/crash

# Ou dans votre navigateur
http://VOTRE_IP/crash
```

**4. Observer le Comportement**

```bash
# Voir les logs PM2
sudo pm2 logs

# Vous devriez voir :
# Error: Intentional crash!
# PM2: App [sample-app] will restart in 100ms

# Statut PM2
sudo pm2 status

# Colonne "↺" (restarts) devrait augmenter
```

---

#### Résultat Attendu

```
✅ App crash détecté par PM2
✅ Redémarrage automatique en ~100ms
✅ App disponible à nouveau
✅ Compteur de restarts incrémenté

Comparaison avec approche basique :
❌ Sans PM2 : App down définitivement
✅ Avec PM2 : Downtime < 1 seconde
```

---

**5. Restaurer l'App Originale**

```bash
sudo pm2 stop sample-app
sudo pm2 delete sample-app
sudo pm2 start /opt/sample-app/app.js --name sample-app
sudo pm2 save
exit
```

---

### Exercice 2 : Test de Redémarrage VM

#### Objectif

Vérifier que l'application redémarre automatiquement après un reboot de la VM.

---

#### Actions

**1. Redémarrer la VM**

**Via Interface :**

```
VM instances
→ Sélectionner sample-app-vm (checkbox)
→ Bouton "RESET" (en haut)
→ Confirmer
```

**Via Cloud Shell :**

```bash
gcloud compute instances reset sample-app-vm --zone=us-central1-a
```

**2. Observer l'État**

```
État : RUNNING → STOPPING → PROVISIONING → RUNNING
Temps : ~30-60 secondes
```

**3. Attendre 2 Minutes**

```
Laisser le temps au startup script de s'exécuter
```

**4. Tester l'Application**

```
Navigateur : http://VOTRE_IP
```

---

#### Question

**L'application fonctionne-t-elle après le reboot ?**

<details>
<summary>💡 Cliquez pour voir la réponse</summary>

### Réponse : ✅ OUI !

**Pourquoi ?**

```
Différence GCP vs AWS :

AWS User Data :
❌ Exécution UNE SEULE FOIS (premier boot)
→ Après reboot : Script ne réexécute pas
→ App non redémarrée automatiquement

GCP Startup Script :
✅ Exécution À CHAQUE BOOT
→ Après reboot : Script s'exécute à nouveau
→ App redémarrée automatiquement

En plus, avec PM2 :
✅ pm2 startup systemd configuré
✅ PM2 démarre avant l'app
✅ PM2 lit la config sauvegardée (pm2 save)
✅ PM2 relance toutes les apps

Double sécurité :
1. Startup Script relance l'app
2. PM2 startup relance aussi l'app
→ Résilience maximale !
```

---

### Vérification

**SSH dans la VM :**

```bash
gcloud compute ssh sample-app-vm --zone=us-central1-a

# Vérifier uptime de la VM
uptime
# Output : up 2 minutes (VM a redémarré récemment)

# Vérifier PM2
sudo pm2 status
# App devrait être "online"

# Vérifier logs startup script
sudo cat /var/log/startup-script.log | tail -20
# Devrait montrer "Startup Script Completed Successfully!"

exit
```

---

### Leçon Importante

```
GCP Startup Script > AWS User Data pour la résilience :

✅ Avantage GCP :
→ Réexécution à chaque boot
→ App toujours redémarrée
→ Moins de configuration manuelle

⚠️ Considération :
→ Script doit être idempotent (peut s'exécuter plusieurs fois)
→ Attention aux installations multiples
→ Utiliser des checks (if not installed, then install)

Best Practice :
→ GCP : Startup Script + PM2
→ AWS : User Data + Systemd Service
→ Les deux : Container orchestration (Kubernetes)
```

</details>

---

### Exercice 3 : Explorer Cloud Logging

#### Objectif

Comprendre les outils de monitoring GCP et comparer avec CloudWatch (AWS).

---

#### Actions

**1. Accéder à Cloud Logging**

```
Navigation Menu (☰)
→ Logging (ou "Operations" → "Logging")
→ Logs Explorer
```

**2. Filtrer les Logs de la VM**

```
Dans la barre de recherche :

resource.type="gce_instance"
resource.labels.instance_id="VOTRE_INSTANCE_ID"

OU simplement :

logName="projects/VOTRE_PROJECT/logs/syslog"
```

**3. Voir les Logs du Startup Script**

```
Filtre :

jsonPayload.message=~"startup-script"

OU

textPayload=~"Installing Node.js"
```

**4. Créer une Metric Basée sur les Logs**

```
1. Dans Logs Explorer, cliquer "Actions" → "Create metric"
2. Configuration :
   - Metric Type : Counter
   - Filter : textPayload=~"Startup Script Completed"
   - Name : startup_script_success
3. CREATE METRIC
```

---

#### Cloud Monitoring (Anciennement Stackdriver)

**Accéder aux Métriques :**

```
Navigation Menu (☰)
→ Monitoring (ou "Operations" → "Monitoring")
→ Metrics Explorer
```

**Métriques Disponibles :**

| Métrique | Catégorie | Description |
|----------|-----------|-------------|
| **CPU utilization** | VM Instance | % utilisation CPU |
| **Disk read bytes** | VM Instance | Lecture disque (bytes/s) |
| **Network bytes sent** | VM Instance | Trafic réseau sortant |
| **Memory usage** | Agent requis | RAM utilisée |

**Visualiser CPU :**

```
1. Resource type : VM Instance
2. Metric : compute.googleapis.com/instance/cpu/utilization
3. Filter : instance_name = sample-app-vm
4. Aggregator : mean
5. Group by : instance_name
6. Time range : 1 hour
```

---

#### Créer un Dashboard

```
1. Monitoring → Dashboards → CREATE DASHBOARD
2. Name : "Sample App Monitoring"
3. ADD CHART
4. Configuration :
   - Title : CPU Utilization
   - Resource : VM Instance
   - Metric : CPU utilization
   - Filter : sample-app-vm
5. SAVE
6. Ajouter d'autres charts (Network, Disk, etc.)
```

---

#### Configurer une Alerte

```
1. Monitoring → Alerting → CREATE POLICY
2. Configuration :
```

| Paramètre | Valeur |
|-----------|--------|
| **Target** | VM Instance → CPU utilization |
| **Filter** | instance_name = sample-app-vm |
| **Condition** | CPU > 80% for 5 minutes |
| **Notification** | Email : votre-email@gmail.com |

```
3. SAVE
```

---

#### Comparaison GCP vs AWS

<details>
<summary>💡 Cliquez pour voir la comparaison</summary>

| Aspect | GCP Cloud Logging/Monitoring | AWS CloudWatch |
|--------|------------------------------|----------------|
| **Logs** | Gratuit (50 GB/mois) | Payant (5 GB gratuit) |
| **Retention** | 30 jours (configurable) | Configurable (coût) |
| **Métriques** | Gratuit (up to 150 MB/mois) | 10 métriques gratuit |
| **Interface** | Logs Explorer (moderne) | CloudWatch Insights (complexe) |
| **Recherche** | BigQuery integration | CloudWatch Logs Insights |
| **Alertes** | Gratuites | 10 alarmes gratuites |
| **Dashboards** | Illimité gratuit | 3 dashboards gratuits |
| **Agent** | Optional (memory metrics) | Optional (detailed metrics) |

---

### Forces de GCP

```
✅ Logs gratuits (50 GB/mois vs 5 GB AWS)
✅ Interface plus moderne et intuitive
✅ BigQuery pour analyse avancée
✅ Dashboards illimités gratuits
✅ Trace et Debugger intégrés

Exemple Pricing :
→ GCP : 50 GB logs/mois = GRATUIT
→ AWS : 50 GB logs/mois = ~$25/mois
```

---

### Forces d'AWS

```
✅ Plus mature (lancé 2009 vs 2014)
✅ Plus de métriques prêtes à l'emploi
✅ Intégration avec tous services AWS
✅ CloudWatch Contributor Insights
✅ Anomaly Detection natif

Exemple :
→ AWS : Lambda logs automatiques
→ GCP : Cloud Functions logs automatiques
→ Équivalent mais AWS plus de services
```

---

### Utilisation Multi-Cloud

```
Stratégie :
→ GCP : Analytics (BigQuery), ML, Logs
→ AWS : Compute (EC2), Storage (S3), CDN
→ Logs envoyés vers Datadog/Splunk
→ Métriques agrégées dans Grafana

Outils Tiers :
→ Datadog (monitoring multi-cloud)
→ New Relic (APM)
→ Grafana + Prometheus
→ ELK Stack (Elasticsearch, Logstash, Kibana)
```

</details>

---

## 🔧 Dépannage

### Problème 1 : Connection Timeout

#### Symptôme

```
Erreur navigateur :
"Ce site est inaccessible"
"ERR_CONNECTION_TIMED_OUT"
```

---

#### Causes et Solutions

**Cause 1 : Règle de Firewall Absente** ⭐⭐⭐⭐⭐

**Vérifier :**

```bash
gcloud compute firewall-rules list --filter="targetTags:http-server"
```

**Si vide ou pas de règle pour port 80 :**

```bash
# Créer la règle de firewall
gcloud compute firewall-rules create allow-http \
  --allow=tcp:80 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server \
  --description="Allow HTTP traffic"

# Ajouter le tag à la VM
gcloud compute instances add-tags sample-app-vm \
  --zone=us-central1-a \
  --tags=http-server
```

---

**Cause 2 : VM pas encore Prête** ⭐⭐⭐

```
Solution :
→ Attendre 3-4 minutes après création
→ Vérifier status : gcloud compute instances list
→ Doit être RUNNING
```

---

**Cause 3 : Startup Script a Échoué** ⭐⭐

**Vérifier les logs :**

```bash
# SSH dans la VM
gcloud compute ssh sample-app-vm --zone=us-central1-a

# Voir logs startup
sudo cat /var/log/startup-script.log

# Chercher erreurs
sudo cat /var/log/startup-script.log | grep -i error

# Vérifier PM2
sudo pm2 status

# Si app pas listée → Startup script a échoué
# Relancer manuellement :
cd /opt/sample-app
sudo pm2 start app.js --name sample-app
sudo pm2 save

exit
```

---

**Cause 4 : Port 80 déjà
