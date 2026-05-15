"""
Producer Kafka - GitHub Archive
===============================
Ce module telecharge les fichiers horaires de GitHub Archive,
parse les evenements JSON ligne par ligne, et les envoie
dans un topic Kafka pour traitement en aval par Spark.

Architecture :
    GH Archive (HTTPS) --> Producer Python --> Kafka (github.raw.events)

Auteur : Samba DIALLO
"""

import gzip
import json
import logging
import os
import sys
import tempfile
import time
from typing import List, Optional

import requests
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# -- Configuration du logging --
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("gh_producer")

# -- Constantes --
GH_ARCHIVE_BASE_URL = "https://data.gharchive.org"

# Types d'evenements GitHub a conserver (filtrage a la source)
ALLOWED_EVENT_TYPES = {
    "PushEvent",
    "PullRequestEvent",
    "WatchEvent",
    "ForkEvent",
    "IssuesEvent",
    "ReleaseEvent",
}

# Fichiers horaires a ingerer (4 heures consecutives pour volume suffisant)
DEFAULT_HOURS = [
    "2025-01-15-10",
    "2025-01-15-11",
    "2025-01-15-12",
    "2025-01-15-13",
]

# -- Configuration Kafka (via variables d'environnement) --
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "github.raw.events")
KAFKA_DLQ_TOPIC = os.environ.get("KAFKA_DLQ_TOPIC", "github.dlq")


def create_kafka_producer(
    bootstrap_servers: str,
    max_retries: int = 10,
    retry_interval: int = 5,
) -> KafkaProducer:
    """
    Cree une instance de KafkaProducer avec gestion des tentatives de reconnexion.

    Le Producer attend que le broker Kafka soit disponible avant de se connecter.
    Cette strategie de retry est necessaire car dans Docker Compose, le Producer
    peut demarrer avant que Kafka soit completement operationnel.

    Args:
        bootstrap_servers: Adresse du broker Kafka (ex: "kafka:29092").
        max_retries: Nombre maximum de tentatives de connexion.
        retry_interval: Delai en secondes entre chaque tentative.

    Returns:
        Instance KafkaProducer configuree et prete a l'envoi.

    Raises:
        SystemExit: Si le broker reste indisponible apres toutes les tentatives.
    """
    for attempt in range(1, max_retries + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                # Garantir la livraison des messages (acquittement complet)
                acks="all",
                # Taille maximale d'un message (10 Mo)
                max_request_size=10485760,
                # Regrouper les messages par lots pour ameliorer le debit
                batch_size=65536,
                linger_ms=100,
            )
            logger.info(
                "Connexion au broker Kafka reussie (tentative %d/%d)",
                attempt,
                max_retries,
            )
            return producer
        except NoBrokersAvailable:
            logger.warning(
                "Broker Kafka indisponible, nouvelle tentative dans %ds (%d/%d)",
                retry_interval,
                attempt,
                max_retries,
            )
            time.sleep(retry_interval)

    logger.critical("Impossible de se connecter a Kafka apres %d tentatives.", max_retries)
    sys.exit(1)


def download_gh_archive(hour: str) -> Optional[str]:
    """
    Telecharge un fichier horaire de GitHub Archive dans un repertoire temporaire.

    Chaque fichier represente une heure d'activite GitHub (~20-100 Mo compresse).
    Le fichier est telecharge en streaming pour limiter l'utilisation memoire.

    Args:
        hour: Identifiant horaire au format "YYYY-MM-DD-H" (ex: "2025-01-15-10").

    Returns:
        Chemin absolu du fichier telecharge, ou None en cas d'echec.
    """
    url = f"{GH_ARCHIVE_BASE_URL}/{hour}.json.gz"
    logger.info("Telechargement de %s ...", url)

    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()

        # Ecriture dans un fichier temporaire pour eviter la corruption
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".json.gz",
            prefix=f"gharchive_{hour}_",
            delete=False,
        )
        downloaded_bytes = 0
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
            downloaded_bytes += len(chunk)
        temp_file.close()

        size_mb = downloaded_bytes / (1024 * 1024)
        logger.info("Fichier telecharge : %s (%.1f Mo)", temp_file.name, size_mb)
        return temp_file.name

    except requests.RequestException as exc:
        logger.error("Echec du telechargement pour l'heure %s : %s", hour, exc)
        return None


def parse_and_produce(
    filepath: str,
    producer: KafkaProducer,
    topic: str,
    dlq_topic: str,
) -> dict:
    """
    Parse un fichier GH Archive compresse et envoie chaque evenement dans Kafka.

    Le fichier est lu ligne par ligne pour minimiser l'empreinte memoire.
    Seuls les types d'evenements definis dans ALLOWED_EVENT_TYPES sont conserves.
    Les lignes impossibles a parser sont envoyees dans la Dead Letter Queue.

    Args:
        filepath: Chemin vers le fichier .json.gz a traiter.
        producer: Instance KafkaProducer active.
        topic: Nom du topic Kafka de destination.
        dlq_topic: Nom du topic Dead Letter Queue pour les erreurs.

    Returns:
        Dictionnaire de statistiques : nombre d'evenements envoyes, filtres, en erreur.
    """
    stats = {
        "sent": 0,
        "filtered": 0,
        "errors": 0,
    }

    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                # Ligne JSON invalide : envoi dans la Dead Letter Queue
                logger.debug("Erreur de parsing ligne %d : %s", line_number, exc)
                producer.send(
                    dlq_topic,
                    value={"line_number": line_number, "raw": line[:500], "error": str(exc)},
                )
                stats["errors"] += 1
                continue

            # Filtrage par type d'evenement
            event_type = event.get("type", "")
            if event_type not in ALLOWED_EVENT_TYPES:
                stats["filtered"] += 1
                continue

            # Extraction des champs essentiels pour alleger le message
            # On conserve le payload minimal pour eviter les depassements de taille
            message = {
                "id": event.get("id"),
                "type": event_type,
                "actor": event.get("actor", {}).get("login", "unknown"),
                "repo": event.get("repo", {}).get("name", "unknown"),
                "created_at": event.get("created_at"),
                "payload": _extract_minimal_payload(event),
            }

            # Envoi dans Kafka avec le nom du repo comme cle de partitionnement
            # Les evenements du meme repo seront dans la meme partition (ordre garanti)
            producer.send(
                topic,
                key=message["repo"].encode("utf-8"),
                value=message,
            )
            stats["sent"] += 1

            # Log de progression tous les 50 000 evenements
            if stats["sent"] % 50000 == 0:
                logger.info("  ... %d evenements envoyes", stats["sent"])

    # Attendre que tous les messages en buffer soient envoyes
    producer.flush()
    return stats


def _extract_minimal_payload(event: dict) -> dict:
    """
    Extrait un sous-ensemble minimal du payload selon le type d'evenement.

    Le champ 'payload' de GitHub Archive est tres volumineux et polymorphe.
    On n'extrait que les champs utiles pour nos analyses en aval :
    - PushEvent : nombre de commits, messages de commit
    - PullRequestEvent : titre, action, etat
    - Autres : champs de base seulement

    Args:
        event: Evenement GitHub Archive complet.

    Returns:
        Dictionnaire reduit du payload.
    """
    event_type = event.get("type", "")
    payload = event.get("payload", {})

    if event_type == "PushEvent":
        commits = payload.get("commits", [])
        return {
            "size": payload.get("size", 0),
            "commits": [
                {
                    "sha": c.get("sha", ""),
                    "message": c.get("message", "")[:500],
                }
                for c in commits[:10]  # Limiter a 10 commits par push
            ],
        }

    if event_type == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        return {
            "action": payload.get("action", ""),
            "title": pr.get("title", "")[:300],
            "body": (pr.get("body") or "")[:500],
            "state": pr.get("state", ""),
            "merged": pr.get("merged", False),
        }

    if event_type == "IssuesEvent":
        issue = payload.get("issue", {})
        return {
            "action": payload.get("action", ""),
            "title": issue.get("title", "")[:300],
        }

    if event_type == "ReleaseEvent":
        release = payload.get("release", {})
        return {
            "action": payload.get("action", ""),
            "tag_name": release.get("tag_name", ""),
        }

    # WatchEvent, ForkEvent : pas de payload specifique utile
    return {}


def run(hours: List[str]) -> None:
    """
    Point d'entree principal du Producer.

    Pour chaque heure specifiee :
    1. Telecharge le fichier GH Archive
    2. Parse et envoie les evenements dans Kafka
    3. Supprime le fichier temporaire pour liberer l'espace disque

    Args:
        hours: Liste des identifiants horaires a traiter.
    """
    logger.info("=== Demarrage du Producer GitHub Archive ===")
    logger.info("Broker Kafka : %s", KAFKA_BOOTSTRAP_SERVERS)
    logger.info("Topic cible  : %s", KAFKA_TOPIC)
    logger.info("Heures a traiter : %s", hours)

    producer = create_kafka_producer(KAFKA_BOOTSTRAP_SERVERS)

    total_stats = {"sent": 0, "filtered": 0, "errors": 0}

    for hour in hours:
        logger.info("--- Traitement de l'heure : %s ---", hour)

        # Etape 1 : Telechargement
        filepath = download_gh_archive(hour)
        if filepath is None:
            logger.error("Impossible de traiter l'heure %s, passage a la suivante.", hour)
            continue

        # Etape 2 : Parsing et envoi dans Kafka
        stats = parse_and_produce(filepath, producer, KAFKA_TOPIC, KAFKA_DLQ_TOPIC)
        logger.info(
            "Heure %s terminee : %d envoyes, %d filtres, %d erreurs",
            hour,
            stats["sent"],
            stats["filtered"],
            stats["errors"],
        )

        # Etape 3 : Nettoyage du fichier temporaire
        try:
            os.unlink(filepath)
            logger.info("Fichier temporaire supprime : %s", filepath)
        except OSError as exc:
            logger.warning("Impossible de supprimer %s : %s", filepath, exc)

        # Accumulation des statistiques globales
        for key in total_stats:
            total_stats[key] += stats[key]

    # Fermeture propre du Producer
    producer.close()

    logger.info("=== Production terminee ===")
    logger.info(
        "Total : %d envoyes, %d filtres, %d erreurs",
        total_stats["sent"],
        total_stats["filtered"],
        total_stats["errors"],
    )


if __name__ == "__main__":
    # Possibilite de surcharger les heures via variable d'environnement
    # Format attendu : "2025-01-15-10,2025-01-15-11,2025-01-15-12,2025-01-15-13"
    hours_env = os.environ.get("GH_ARCHIVE_HOURS", "")
    if hours_env:
        hours_to_process = [h.strip() for h in hours_env.split(",") if h.strip()]
    else:
        hours_to_process = DEFAULT_HOURS

    run(hours_to_process)
