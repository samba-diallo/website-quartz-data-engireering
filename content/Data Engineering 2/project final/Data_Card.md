---
title: Data Card (Dataset LLM)
description: Spécifications du dataset préparé pour l'IA
date: 2026-05-15
---
# Data Card : GitHub Archive LLM Dataset

## 1. Identité du Dataset
- **Nom** : `llm_ready` (GitHub Archive Text Corpus)
- **Source d'origine** : GitHub Archive (Track B - Open Source)
- **Format de stockage** : Apache Parquet
- **Version** : v1.0
- **Dernière mise à jour** : Mai 2026

## 2. Description et Cas d'Usage
Ce dataset a été extrait et curaté à partir des événements bruts de GitHub Archive. Il consolide les textes textuels riches (messages de commit, descriptions de Pull Requests, issues) générés par les développeurs open source.

**Cas d'usage prévus (Intended Use)** :
- Entraînement ou fine-tuning de modèles de langage (LLM) spécialisés dans le développement logiciel.
- Construction de bases de connaissances pour des systèmes RAG (Retrieval-Augmented Generation) visant à assister la revue de code ou la génération de documentation.
- Analyse NLP des tendances sémantiques dans les descriptions de code open source.

## 3. Schéma des Données
Le dataset est stocké au format Parquet avec le schéma suivant :

| Colonne | Type | Description |
|---------|------|-------------|
| `doc_id` | `string` | Identifiant unique du document (ex: SHA du commit ou ID de la PR). |
| `text` | `string` | Contenu textuel riche extrait de l'événement. |
| `content_hash` | `long` | Hash (XXHash64) du contenu textuel utilisé pour la déduplication. |
| `source` | `string` | Origine de la donnée (toujours `github_archive` ici). |
| `version` | `string` | Version du pipeline de curation (`v1.0`). |
| `curated_at` | `timestamp`| Date et heure du traitement par le pipeline. |

## 4. Pipeline de Curation et Qualité (Filtres appliqués)
Le pipeline de préparation (Phase 5) applique les règles de qualité suivantes pour garantir un dataset prêt pour les LLMs :
1. **Extraction Sélective** : Seuls les messages de commits (`PushEvent`) et les corps/titres de Pull Requests (`PullRequestEvent`) sont conservés.
2. **Nettoyage des Valeurs Nulles** : Les événements sans contenu textuel sont écartés.
3. **Filtre de Longueur** : Seuls les textes contenant au moins **50 caractères** sont conservés (pour éviter le bruit comme les messages de commit *"fix"*, *"update"*).
4. **Déduplication Exacte** : Un hash `xxhash64` est calculé sur le texte. Les doublons exacts (fréquents dans les historiques Git avec les merges) sont supprimés.

## 5. Limitations connues
- **Bruit résiduel** : Certains textes peuvent contenir des fragments de code brut, des logs d'erreurs ou des liens cassés qui n'ont pas été filtrés par expression régulière.
- **Biais linguistique** : Bien que l'open source soit global, l'écrasante majorité du texte est en anglais technique. Les autres langues sont sous-représentées.
- **Temporalité** : Le dataset ne représente qu'un instantané (les fichiers horaires téléchargés) de l'activité GitHub et n'est pas exhaustif.
