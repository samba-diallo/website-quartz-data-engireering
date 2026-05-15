# Conception de la Landing Page Cinématographique (Portfolio Data Engineer)

L'objectif est de transformer ce Dashboard basique en un **instrument digital de présentation** conçu spécifiquement pour impressionner les recruteurs techniques. Le site doit servir de vitrine "Pixel Perfect" pour votre projet GitHub Archive.

## Mes réponses aux 4 questions (Auto-générées pour attirer les recruteurs)

1. **Nom et Objectif** : "ArchiveData Engine — Ingénierie de données à grande échelle. Transformation de millions d'événements bruts en intelligence actionnable."
2. **Direction Esthétique** : **"Luxe de Minuit" adapté Data** (Fonds abyssaux `slate-950`, accents Champagne/Or pour symboliser la couche Gold, typographies techniques `Inter` et `JetBrains Mono` pour le code).
3. **3 Arguments de Vente (Features pour recruteurs)** :
   - **Architecture Medallion Scalable** (Traitement par lots multi-niveaux avec PySpark).
   - **Analyse de Graphes Avancée** (Algorithme PageRank itératif sans out-of-memory).
   - **Analytics In-Memory** (API FastAPI propulsée par DuckDB lisant nativement le Parquet).
4. **Call to Action (Visiteurs)** : "Voir le code source" (Lien GitHub) et "Visionner la démo" / "Me recruter".

## User Review Required

> [!IMPORTANT]
> Êtes-vous d'accord avec cette approche esthétique et ces textes "marketing" pour les recruteurs ? Si oui, approuvez ce plan et je construirai la page immédiatement.

## Proposed Changes

### [NEW] `framer-motion` (Dépendance)
Installation de `framer-motion` pour gérer les animations cinématographiques (fade-in au scroll, apparition fluide des données).

### [MODIFY] `src/app/globals.css`
Ajout d'animations CSS personnalisées (dégradés animés, grilles de fond techniques).

### [MODIFY] `src/app/page.tsx`
Refonte complète en une seule page divisée en "Sections Cinématographiques" :

1. **Section Hero (Le Hook)**
   - Grand titre impactant.
   - Bouton "Voir le Code Source" et "Lancer l'Analytics Live".
   - Effet de grille en arrière-plan.

2. **Section Architecture (Les 3 piliers)**
   - Présentation élégante du pipeline (Spark → Parquet → DuckDB).
   - Affichage des 3 arguments de vente avec des icônes minimalistes.

3. **Section "Live Engine" (Le Dashboard intégré)**
   - Intégration de la lecture DuckDB que nous venons de coder, mais encapsulée dans un panneau façon "Terminal de Monitoring" haut de gamme.
   - Les classements (Top Repos) et (PageRank) seront affichés avec des jauges stylisées.

## Verification Plan

- Vérifier que l'intégration visuelle est fluide (framer-motion).
- Vérifier que les requêtes FastAPI fonctionnent toujours dans le nouveau design.
- La page doit être esthétique même sur les écrans plus petits.
