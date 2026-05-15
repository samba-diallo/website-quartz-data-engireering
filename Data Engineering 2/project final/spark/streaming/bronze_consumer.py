"""
Consumer Spark Structured Streaming - Couche Bronze
====================================================
Ce module lit les evenements GitHub depuis le topic Kafka
et les ecrit en format Parquet dans la couche Bronze du Lakehouse.

Architecture :
    Kafka (github.raw.events) --> Spark Structured Streaming --> Bronze (Parquet)

Le streaming fonctionne en mode micro-batch avec un trigger intervalle
de 30 secondes, conforme au SLO de latence streaming du projet.

Auteur : Samba DIALLO
"""

import os
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    current_timestamp,
    to_date,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    BooleanType,
    IntegerType,
)

# -- Configuration du logging --
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("bronze_consumer")

# -- Configuration via variables d'environnement --
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "github.raw.events")
BRONZE_OUTPUT_PATH = os.environ.get("BRONZE_OUTPUT_PATH", "outputs/project/bronze_v2")
CHECKPOINT_PATH = os.environ.get("CHECKPOINT_PATH", "outputs/project/bronze_v2_checkpoint")

# -- Schema JSON des evenements produits par le Producer Kafka --
# Ce schema correspond exactement a la structure emise par gh_producer.py
COMMIT_SCHEMA = StructType([
    StructField("sha", StringType(), True),
    StructField("message", StringType(), True),
])

PAYLOAD_SCHEMA = StructType([
    # Champs PushEvent
    StructField("size", IntegerType(), True),
    StructField("commits", ArrayType(COMMIT_SCHEMA), True),
    # Champs PullRequestEvent
    StructField("action", StringType(), True),
    StructField("title", StringType(), True),
    StructField("body", StringType(), True),
    StructField("state", StringType(), True),
    StructField("merged", BooleanType(), True),
    # Champs ReleaseEvent
    StructField("tag_name", StringType(), True),
])

EVENT_SCHEMA = StructType([
    StructField("id", StringType(), True),
    StructField("type", StringType(), True),
    StructField("actor", StringType(), True),
    StructField("repo", StringType(), True),
    StructField("created_at", StringType(), True),
    StructField("payload", PAYLOAD_SCHEMA, True),
])


def create_spark_session() -> SparkSession:
    """
    Cree et configure la session Spark pour la lecture Kafka.

    La configuration inclut les packages necessaires pour la connectivite Kafka
    et les reglages de performance adaptes a un environnement local.

    Returns:
        Session Spark configuree.
    """
    spark = (
        SparkSession.builder
        .appName("DE2_Bronze_Consumer")
        .master("local[*]")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.streaming.stopGracefullyOnShutdown", "true")
        .getOrCreate()
    )

    # Reduire la verbosity des logs Spark
    spark.sparkContext.setLogLevel("WARN")
    return spark


def start_bronze_streaming(spark: SparkSession) -> None:
    """
    Demarre le flux de streaming Kafka -> Bronze.

    Le consumer lit les messages depuis le topic Kafka, parse le JSON,
    ajoute des metadonnees d'ingestion (timestamp, date de partition),
    et ecrit les resultats en Parquet partitionne par date.

    Args:
        spark: Session Spark active.
    """
    logger.info("Configuration du flux Kafka -> Bronze")
    logger.info("  Broker Kafka : %s", KAFKA_BOOTSTRAP_SERVERS)
    logger.info("  Topic source : %s", KAFKA_TOPIC)
    logger.info("  Sortie Bronze : %s", BRONZE_OUTPUT_PATH)

    # Lecture du flux Kafka
    raw_stream = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
        .option("subscribe", KAFKA_TOPIC)
        # Commencer depuis le debut du topic pour retraiter tout l'historique
        .option("startingOffsets", "earliest")
        # Taille maximale par micro-batch pour controler la charge memoire
        .option("maxOffsetsPerTrigger", 100000)
        .load()
    )

    # Conversion du message Kafka (binaire) en JSON structure
    parsed_stream = (
        raw_stream
        .select(
            # Cle de partitionnement Kafka (nom du repo)
            col("key").cast("string").alias("kafka_key"),
            # Parsing du corps du message JSON selon notre schema
            from_json(col("value").cast("string"), EVENT_SCHEMA).alias("event"),
            # Metadonnees Kafka pour le debugging et l'audit
            col("topic").alias("kafka_topic"),
            col("partition").alias("kafka_partition"),
            col("offset").alias("kafka_offset"),
            col("timestamp").alias("kafka_timestamp"),
        )
        .select(
            # Aplatissement des champs de l'evenement
            col("event.id").alias("event_id"),
            col("event.type").alias("event_type"),
            col("event.actor").alias("actor_login"),
            col("event.repo").alias("repo_name"),
            col("event.created_at").alias("created_at"),
            col("event.payload").alias("payload"),
            # Metadonnees d'ingestion
            col("kafka_partition"),
            col("kafka_offset"),
            col("kafka_timestamp"),
            # Timestamp d'ingestion Bronze (quand le record est ecrit)
            current_timestamp().alias("ingested_at"),
            # Date de partition pour l'ecriture partitionnee
            to_date(col("event.created_at")).alias("date"),
        )
    )

    # Ecriture en Parquet partitionne par date
    query = (
        parsed_stream
        .writeStream
        .format("parquet")
        .outputMode("append")
        # Trigger toutes les 30 secondes (conforme au SLO streaming)
        .trigger(processingTime="30 seconds")
        .option("checkpointLocation", CHECKPOINT_PATH)
        .option("path", BRONZE_OUTPUT_PATH)
        .partitionBy("date")
        .queryName("bronze_kafka_consumer")
        .start()
    )

    logger.info("Flux Bronze demarre. En attente de donnees...")
    logger.info("Arret propre avec Ctrl+C")

    # Attente de terminaison (le streaming tourne indefiniment)
    query.awaitTermination()


def main() -> None:
    """Point d'entree principal du consumer Bronze."""
    logger.info("=== Demarrage du Consumer Bronze (Kafka -> Parquet) ===")

    spark = create_spark_session()

    try:
        start_bronze_streaming(spark)
    except KeyboardInterrupt:
        logger.info("Arret du consumer demande par l'utilisateur.")
    finally:
        spark.stop()
        logger.info("Session Spark fermee proprement.")


if __name__ == "__main__":
    main()
