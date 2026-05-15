#!/bin/bash
# ==========================================================
# Script d'initialisation des topics Kafka
# Ce script attend que Kafka soit pret, puis cree les topics
# necessaires au pipeline GitHub Archive.
# ==========================================================

KAFKA_BROKER="kafka:29092"
MAX_RETRIES=30
RETRY_INTERVAL=2

echo "[init_topics] Attente de la disponibilite du broker Kafka..."

# Boucle de verification : on attend que Kafka reponde
for i in $(seq 1 $MAX_RETRIES); do
    kafka-topics --bootstrap-server "$KAFKA_BROKER" --list > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[init_topics] Kafka est pret (tentative $i/$MAX_RETRIES)."
        break
    fi
    echo "[init_topics] Kafka pas encore pret, nouvelle tentative dans ${RETRY_INTERVAL}s... ($i/$MAX_RETRIES)"
    sleep $RETRY_INTERVAL
done

# ---- Creation des topics ----

# Topic principal : evenements bruts GitHub Archive (JSON complet)
kafka-topics --bootstrap-server "$KAFKA_BROKER" \
    --create --if-not-exists \
    --topic github.raw.events \
    --partitions 3 \
    --replication-factor 1 \
    --config retention.ms=86400000

# Topic Dead Letter Queue : messages impossibles a parser
kafka-topics --bootstrap-server "$KAFKA_BROKER" \
    --create --if-not-exists \
    --topic github.dlq \
    --partitions 1 \
    --replication-factor 1 \
    --config retention.ms=604800000

echo "[init_topics] Topics crees avec succes :"
kafka-topics --bootstrap-server "$KAFKA_BROKER" --list

echo "[init_topics] Initialisation terminee."
