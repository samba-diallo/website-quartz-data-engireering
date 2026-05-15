Je veux que tu analyses complètement l’architecture actuelle de mon repository avant toute modification ou publication sur GitHub.

IMPORTANT :
Tu dois agir comme :

* un expert DevSecOps
* un architecte Data Engineering
* un expert Git/GitHub
* un expert sécurité secrets management
* un expert CI/CD

Tu dois utiliser le contexte réel du repository via MCP GitHub afin d’inspecter toute la structure existante avant que nous commencions à pousser davantage de code ou de config.

L’objectif principal est de :

* sécuriser complètement le projet
* éviter toute fuite de secrets
* éviter de publier des tokens/API keys
* préparer une architecture propre et professionnelle
* préparer un monorepo Data Engineering moderne

IMPORTANT :
Tu ne dois PAS encore modifier massivement le projet.
Tu dois d’abord faire un audit complet.

---

# Ce que je veux que tu analyses

Analyse :

* l’architecture globale du repository
* les dossiers existants
* les fichiers sensibles
* les workflows GitHub Actions
* les fichiers de configuration
* les fichiers cachés
* les fichiers `.env`
* les dépendances
* les configurations Docker
* les configs Quartz
* les configs frontend/backend
* les secrets potentiellement exposés
* les clés/API tokens hardcodés
* les mauvaises pratiques sécurité

---

# Audit sécurité attendu

Je veux que tu vérifies :

## Secrets potentiellement exposés

Recherche :

* tokens GitHub
* API keys
* credentials
* secrets cloud
* mots de passe
* JWT secrets
* private keys
* `.pem`
* `.p12`
* `.key`
* `.env`
* `.env.local`
* `.secrets`
* variables hardcodées

---

# Git hygiene

Vérifie :

* `.gitignore`
* fichiers trackés dangereux
* fichiers qui ne devraient pas être commit
* dossiers à exclure
* caches
* datasets volumineux
* logs
* builds
* dépendances locales

---

# Docker / Infrastructure

Vérifie :

* docker-compose
* variables d’environnement
* ports exposés
* credentials Docker
* volumes sensibles

---

# GitHub Actions

Analyse :

* workflows CI/CD
* secrets GitHub Actions
* permissions excessives
* mauvaises pratiques sécurité

---

# Quartz / Frontend / Backend

Vérifie :

* configs publiques dangereuses
* URLs hardcodées
* variables sensibles exposées côté frontend
* fichiers buildés à ignorer

---

# Ce que je veux dans la réponse

Je veux un rapport extrêmement structuré contenant :

## 1. État actuel du repository

* structure actuelle
* organisation actuelle
* points positifs
* points problématiques

---

## 2. Audit sécurité complet

* secrets détectés
* risques potentiels
* fichiers dangereux
* configs dangereuses
* éléments à sécuriser

---

## 3. Recommandations `.gitignore`

Je veux un `.gitignore` professionnel adapté à :

* Python
* Spark
* Kafka
* Node.js
* Next.js
* Quartz
* Docker
* dbt
* Airflow
* VS Code

---

## 4. Stratégie secrets management

Je veux :

* où stocker les tokens
* comment utiliser `.env`
* quelles variables utiliser
* comment sécuriser GitHub Actions
* comment éviter les leaks

---

## 5. Architecture monorepo recommandée

Je veux une proposition propre pour organiser :

* Quartz
* frontend-dashboard
* backend
* Kafka
* Spark
* dbt
* Airflow
* infrastructure
* scripts

---

## 6. Stratégie Git/GitHub

Je veux :

* quoi pousser sur GitHub
* quoi ne jamais pousser
* quelles branches utiliser
* comment gérer les secrets
* comment gérer les datasets
* comment gérer les fichiers temporaires

---

## 7. Checklist sécurité avant push GitHub

Je veux une checklist finale contenant :

* validations à effectuer
* fichiers à vérifier
* commandes Git utiles
* contrôles sécurité avant commit

---

IMPORTANT :
Tu dois d’abord AUDITER et ANALYSER.

Tu ne dois PAS encore :

* refactoriser massivement
* déplacer tous les fichiers
* réécrire le projet

Je veux d’abord comprendre :

* l’état actuel
* les risques
* la meilleure stratégie de structuration
* la meilleure stratégie sécurité

avant de commencer les grosses modifications du projet.
