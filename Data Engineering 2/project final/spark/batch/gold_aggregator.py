"""
Transformation Spark Batch - Couche Gold
========================================
Ce module lit les donnees nettoyees de la couche Silver
et produit des tables analytiques agregees dans la couche Gold.

Tables Gold produites :
    1. repo_activity    : agregation par repo, date et type d'evenement
    2. pagerank         : score d'influence PageRank iteratif
    3. hourly_activity  : activite par heure (pour le dashboard temps reel)

Architecture :
    Silver (Parquet) --> Spark Batch --> Gold (Parquet)

Auteur : Samba DIALLO
"""

import os
import logging

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col,
    count,
    sum as spark_sum,
    hour,
    dayofweek,
    lit,
    when,
    abs as spark_abs,
    broadcast,
)

# -- Configuration du logging --
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("gold_aggregator")

# -- Chemins d'entree et de sortie --
SILVER_PATH = os.environ.get("SILVER_PATH", "outputs/project/silver_v2")
GOLD_PATH = os.environ.get("GOLD_PATH", "outputs/project/gold_v2")

# -- Constantes PageRank --
PAGERANK_DAMPING_FACTOR = 0.85
PAGERANK_MAX_ITERATIONS = 10
PAGERANK_CONVERGENCE_THRESHOLD = 0.001


def create_spark_session() -> SparkSession:
    """
    Cree et configure la session Spark pour le traitement batch Gold.

    Returns:
        Session Spark configuree pour le mode local.
    """
    spark = (
        SparkSession.builder
        .appName("DE2_Gold_Aggregator")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.parquet.compression.codec", "snappy")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def build_repo_activity(spark: SparkSession, silver_df: DataFrame) -> None:
    """
    Construit la table Gold d'activite par depot.

    Agregation des evenements par repo_name, date et event_type
    pour permettre des analyses temporelles dans le dashboard.

    Args:
        spark: Session Spark active.
        silver_df: DataFrame Silver source.
    """
    output_path = os.path.join(GOLD_PATH, "repo_activity")
    logger.info("Construction de la table repo_activity...")

    repo_activity = (
        silver_df
        .groupBy("repo_name", "date", "event_type")
        .agg(count("*").alias("event_count"))
        .orderBy(col("event_count").desc())
    )

    record_count = repo_activity.count()
    logger.info("  repo_activity : %d records", record_count)

    (
        repo_activity
        .repartition(4)
        .write
        .mode("overwrite")
        .parquet(output_path)
    )
    logger.info("  Ecrit dans : %s", output_path)


def build_hourly_activity(spark: SparkSession, silver_df: DataFrame) -> None:
    """
    Construit la table Gold d'activite horaire.

    Cette table permet de visualiser les pics d'activite par heure
    et par jour de la semaine dans le dashboard.

    Args:
        spark: Session Spark active.
        silver_df: DataFrame Silver source.
    """
    output_path = os.path.join(GOLD_PATH, "hourly_activity")
    logger.info("Construction de la table hourly_activity...")

    hourly_df = (
        silver_df
        .withColumn("hour_of_day", hour(col("created_at")))
        .withColumn("day_of_week", dayofweek(col("created_at")))
        .groupBy("hour_of_day", "day_of_week", "event_type")
        .agg(count("*").alias("event_count"))
        .orderBy("hour_of_day", "day_of_week")
    )

    record_count = hourly_df.count()
    logger.info("  hourly_activity : %d records", record_count)

    (
        hourly_df
        .repartition(2)
        .write
        .mode("overwrite")
        .parquet(output_path)
    )
    logger.info("  Ecrit dans : %s", output_path)


def build_pagerank(spark: SparkSession, silver_df: DataFrame) -> None:
    """
    Execute l'algorithme PageRank iteratif sur le graphe Developpeur -> Depot.

    Le graphe est construit a partir des contributions :
    - PushEvent, PullRequestEvent, IssuesEvent representent des aretes
      depuis actor_login (source) vers repo_name (destination).

    L'algorithme distribue iterativement le rang de chaque noeud
    a ses voisins, pondere par un facteur d'amortissement (damping).

    Args:
        spark: Session Spark active.
        silver_df: DataFrame Silver source.
    """
    output_path = os.path.join(GOLD_PATH, "pagerank")
    logger.info("Construction du PageRank iteratif...")

    # Types d'evenements representant des contributions significatives
    contribution_types = ["PushEvent", "PullRequestEvent", "IssuesEvent"]

    # Construction des aretes du graphe : actor_login -> repo_name
    edges = (
        silver_df
        .filter(col("event_type").isin(contribution_types))
        .select(
            col("actor_login").alias("src"),
            col("repo_name").alias("dst"),
        )
        .distinct()
    )

    edge_count = edges.count()
    logger.info("  Aretes du graphe : %d", edge_count)

    if edge_count == 0:
        logger.warning("  Aucune arete trouvee, PageRank ignore.")
        return

    # Extraction de tous les noeuds uniques (acteurs + repos)
    nodes_src = edges.select(col("src").alias("node"))
    nodes_dst = edges.select(col("dst").alias("node"))
    all_nodes = nodes_src.union(nodes_dst).distinct()
    node_count = all_nodes.count()
    logger.info("  Noeuds du graphe : %d", node_count)

    # Initialisation : chaque noeud commence avec un rang egal (1/N)
    initial_rank = 1.0 / node_count
    ranks = all_nodes.withColumn("rank", lit(initial_rank))

    # Nombre de liens sortants par noeud source
    out_degree = edges.groupBy("src").agg(count("*").alias("out_count"))

    # Iterations PageRank
    damping = PAGERANK_DAMPING_FACTOR
    base_rank = (1.0 - damping) / node_count

    for iteration in range(1, PAGERANK_MAX_ITERATIONS + 1):
        # Jointure : chaque arete recoit le rang du noeud source
        contributions = (
            edges
            .join(ranks, edges["src"] == ranks["node"], "inner")
            .join(out_degree, edges["src"] == out_degree["src"], "inner")
            .select(
                edges["dst"].alias("node"),
                (col("rank") / col("out_count")).alias("contribution"),
            )
        )

        # Somme des contributions recues par chaque noeud
        new_ranks = (
            contributions
            .groupBy("node")
            .agg(spark_sum("contribution").alias("sum_contributions"))
            .withColumn("rank", lit(base_rank) + lit(damping) * col("sum_contributions"))
            .select("node", "rank")
        )

        # Les noeuds sans lien entrant conservent le rang de base
        new_ranks = (
            all_nodes
            .join(new_ranks, "node", "left")
            .withColumn("rank", when(col("rank").isNull(), lit(base_rank)).otherwise(col("rank")))
        )

        # Verification de la convergence (delta entre iterations)
        delta_df = (
            ranks.alias("old")
            .join(new_ranks.alias("new"), "node")
            .select(spark_abs(col("old.rank") - col("new.rank")).alias("delta"))
        )
        total_delta = delta_df.agg(spark_sum("delta")).collect()[0][0] or 0.0

        logger.info("  Iteration %d/%d - Delta total : %.6f", iteration, PAGERANK_MAX_ITERATIONS, total_delta)

        ranks = new_ranks

        if total_delta < PAGERANK_CONVERGENCE_THRESHOLD:
            logger.info("  Convergence atteinte a l'iteration %d", iteration)
            break

    # Ecriture des resultats tries par rang decroissant
    (
        ranks
        .select(col("node").alias("src"), col("rank"))
        .orderBy(col("rank").desc())
        .repartition(2)
        .write
        .mode("overwrite")
        .parquet(output_path)
    )
    logger.info("  PageRank ecrit dans : %s", output_path)


def main() -> None:
    """Point d'entree principal de l'agregation Gold."""
    logger.info("=== Demarrage de l'agregation Silver -> Gold ===")

    spark = create_spark_session()

    try:
        # Lecture de la couche Silver
        logger.info("Lecture de la couche Silver : %s", SILVER_PATH)
        silver_df = spark.read.parquet(SILVER_PATH)
        silver_df.cache()
        total_records = silver_df.count()
        logger.info("Records Silver lus : %d", total_records)

        # Construction des tables Gold
        build_repo_activity(spark, silver_df)
        build_hourly_activity(spark, silver_df)
        build_pagerank(spark, silver_df)

        logger.info("=== Agregation Gold terminee avec succes ===")

    except Exception as exc:
        logger.error("Erreur lors de l'agregation Gold : %s", exc, exc_info=True)
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
