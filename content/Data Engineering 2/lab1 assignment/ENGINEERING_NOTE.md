
# DE2 Lab 1: Pipeline de streaming - Note d'ingénierie

## Objectif
Implémente et optimise un pipeline Structured Streaming pour les événements esport OpenDota
avec agrégation par fenêtre, gestion des watermarks, et livraison exactly-once basée sur checkpoints.

## Piste de données: Piste A (Esport/OpenDota)
- Schéma: event_timestamp, team_id, hero_id, gold_earned, kills
- Source d'événements: événements de match OpenDota synthétiques (2000 événements, ~120 sec de durée)
- Durée de la fenêtre: 10 secondes
- Délai du watermark: 5 secondes (tolérance pour données tardives)

## Architecture

### De base (Sans optimisation)
- Lecture du flux avec partition unique
- Agrégation par fenêtre sans repartitionnement
- Sortie: stream_sink_baseline (Parquet)
- Checkpoint: checkpoint_baseline

### Optimisée (Stratégie de repartitionnement)
- Lire le flux et repartitionner par team_id (4 partitions)
- Cette optimisation colocalise les données d'équipe localement, réduisant le coût de shuffle pendant le groupBy
- Agrégation par fenêtre sur données repartitionnées
- Sortie: stream_sink_optimized (Parquet)
- Checkpoint: checkpoint_optimized

## Métriques clés capturées
1. Plans d'exécution de requête (explain formatted)
2. Nombre de lignes de sortie
3. Statistiques d'agrégation (avg event_count, avg total_gold)
4. Répertoires de checkpoint (vérifier livraison exactly-once)

## Observations
- Le repartitionnement avant l'agrégation par fenêtre réduit la surcharge de shuffle
- Le watermark assure que les événements tardifs sont gérés dans la fenêtre de tolérance
- Les répertoires de checkpoint fournissent la tolérance aux pannes et les garanties de récupération

## Reproductibilité
- Graine fixée (42) pour la génération de données synthétiques
- Limites de fenêtre déterministes liées au timestamp
- Configuration matérielle identique supposée
- Tous les artefacts dans le dossier /lab1 assignment

## Fichiers générés
- outputs/lab1/stream_sink_baseline/ : Sortie Parquet (de base)
- outputs/lab1/stream_sink_optimized/ : Sortie Parquet (optimisée)
- outputs/lab1/checkpoint_baseline/ : Checkpoint (de base)
- outputs/lab1/checkpoint_optimized/ : Checkpoint (optimisée)
- proof/plan_baseline.txt : Plan de requête (de base)
- proof/plan_optimized.txt : Plan de requête (optimisée)
- lab1_metrics_log.csv : Comparaison des métriques
