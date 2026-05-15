"""
Transformation Spark Batch - Couche Silver
==========================================
Ce module lit les donnees brutes de la couche Bronze (Parquet)
et produit des donnees nettoyees et typees dans la couche Silver.

Transformations appliquees :
    - Suppression des evenements sans identifiant
    - Normalisation des types et des timestamps
    - Aplatissement partiel du payload (commits, PR)
    - Partitionnement par date pour optimiser les lectures en aval

Architecture :
    Bronze (Parquet) --> Spark Batch --> Silver (Parquet)

Auteur : Samba DIALLO
"""

import os
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_timestamp,
    to_date,
    explode_outer,
    trim,
    when,
    lit,
    current_timestamp,
    size,
)

# -- Configuration du logging --
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("silver_transformer")

# -- Chemins d'entree et de sortie --
BRONZE_PATH = os.environ.get("BRONZE_PATH", "outputs/project/bronze_v2")
SILVER_PATH = os.environ.get("SILVER_PATH", "outputs/project/silver_v2")


def create_spark_session() -> SparkSession:
    """
    Cree et configure la session Spark pour le traitement batch Silver.

    Returns:
        Session Spark configuree pour le mode local.
    """
    spark = (
        SparkSession.builder
        .appName("DE2_Silver_Transformer")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.parquet.compression.codec", "snappy")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def transform_bronze_to_silver(spark: SparkSession) -> None:
    """
    Effectue la transformation Bronze -> Silver.

    Les operations de nettoyage comprennent :
    - Filtrage des records sans event_id (donnees corrompues)
    - Casting du champ created_at en timestamp natif Spark
    - Extraction des commits (PushEvent) en lignes individuelles
    - Extraction des metadonnees de PR (PullRequestEvent)
    - Ajout d'un timestamp de transformation pour l'audit

    Args:
        spark: Session Spark active.
    """
    logger.info("Lecture de la couche Bronze : %s", BRONZE_PATH)

    bronze_df = spark.read.parquet(BRONZE_PATH)
    initial_count = bronze_df.count()
    logger.info("Records Bronze lus : %d", initial_count)

    # -- Nettoyage de base --
    # Suppression des lignes sans identifiant (donnees invalides du parsing)
    cleaned_df = (
        bronze_df
        .filter(col("event_id").isNotNull())
        .filter(col("event_type").isNotNull())
        .withColumn("created_at_ts", to_timestamp(col("created_at")))
        .withColumn("date", to_date(col("created_at_ts")))
        .withColumn("transformed_at", current_timestamp())
    )

    # -- Table Silver principale : evenements nettoyes --
    # On conserve les champs de base sans le payload brut
    silver_events = (
        cleaned_df
        .select(
            col("event_id"),
            col("event_type"),
            col("actor_login"),
            col("repo_name"),
            col("created_at_ts").alias("created_at"),
            col("date"),
            col("transformed_at"),
            # Extraction conditionnelle des champs de payload selon le type
            when(col("event_type") == "PushEvent", col("payload.size"))
                .alias("push_commit_count"),
            when(col("event_type") == "PullRequestEvent", col("payload.action"))
                .alias("pr_action"),
            when(col("event_type") == "PullRequestEvent", col("payload.title"))
                .alias("pr_title"),
            when(col("event_type") == "PullRequestEvent", col("payload.state"))
                .alias("pr_state"),
            when(col("event_type") == "PullRequestEvent", col("payload.merged"))
                .alias("pr_merged"),
            when(col("event_type") == "IssuesEvent", col("payload.action"))
                .alias("issue_action"),
            when(col("event_type") == "IssuesEvent", col("payload.title"))
                .alias("issue_title"),
            when(col("event_type") == "ReleaseEvent", col("payload.tag_name"))
                .alias("release_tag"),
        )
    )

    silver_count = silver_events.count()
    logger.info("Records Silver produits : %d (filtre %d invalides)", silver_count, initial_count - silver_count)

    # Ecriture en Parquet partitionne par date
    (
        silver_events
        .repartition(4, "date")
        .write
        .mode("overwrite")
        .partitionBy("date")
        .parquet(SILVER_PATH)
    )

    logger.info("Couche Silver ecrite dans : %s", SILVER_PATH)

    # -- Table Silver secondaire : commits (pour l'index inverse) --
    # Explose le tableau de commits des PushEvent en lignes individuelles
    commits_path = os.path.join(SILVER_PATH + "_commits")
    push_events = cleaned_df.filter(col("event_type") == "PushEvent")

    # Verifier que des commits existent avant d'exploser
    if push_events.count() > 0:
        commits_df = (
            push_events
            .select(
                col("event_id"),
                col("actor_login"),
                col("repo_name"),
                col("created_at_ts").alias("created_at"),
                col("date"),
                explode_outer(col("payload.commits")).alias("commit"),
            )
            .select(
                col("event_id"),
                col("actor_login"),
                col("repo_name"),
                col("created_at"),
                col("date"),
                col("commit.sha").alias("commit_sha"),
                trim(col("commit.message")).alias("commit_message"),
            )
            .filter(col("commit_message").isNotNull())
            .filter(col("commit_message") != "")
        )

        commit_count = commits_df.count()
        logger.info("Commits individuels extraits : %d", commit_count)

        (
            commits_df
            .repartition(4)
            .write
            .mode("overwrite")
            .parquet(commits_path)
        )
        logger.info("Table des commits ecrite dans : %s", commits_path)


def main() -> None:
    """Point d'entree principal de la transformation Silver."""
    logger.info("=== Demarrage de la transformation Bronze -> Silver ===")

    spark = create_spark_session()

    try:
        transform_bronze_to_silver(spark)
        logger.info("=== Transformation Silver terminee avec succes ===")
    except Exception as exc:
        logger.error("Erreur lors de la transformation Silver : %s", exc, exc_info=True)
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
