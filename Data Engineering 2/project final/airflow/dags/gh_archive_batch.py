"""
DAG Airflow - Pipeline Batch GitHub Archive
============================================
Ce DAG orchestre le pipeline de transformation batch :
    Producer Kafka -> (attente) -> Silver -> Gold

Il est declenche toutes les heures pour traiter les nouvelles donnees
arrivees dans la couche Bronze via le streaming Kafka.

Auteur : Samba DIALLO
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# -- Configuration par defaut du DAG --
default_args = {
    "owner": "samba-diallo",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# Chemins des scripts Spark (relatifs au volume monte dans le container)
SPARK_SCRIPTS_PATH = "/opt/spark/scripts"


def log_pipeline_start(**context):
    """Enregistre le demarrage du pipeline dans les logs Airflow."""
    logical_date = context["logical_date"]
    print(f"[pipeline] Demarrage du pipeline batch pour : {logical_date}")
    print(f"[pipeline] Heure logique de traitement : {logical_date.strftime('%Y-%m-%d-%H')}")


with DAG(
    dag_id="gh_archive_batch_pipeline",
    default_args=default_args,
    description="Pipeline batch Bronze -> Silver -> Gold pour les donnees GitHub Archive",
    schedule_interval="@hourly",
    start_date=datetime(2025, 1, 15),
    catchup=False,
    max_active_runs=1,
    tags=["github-archive", "batch", "etl"],
) as dag:

    # Tache 1 : Journalisation du demarrage
    start_task = PythonOperator(
        task_id="log_pipeline_start",
        python_callable=log_pipeline_start,
    )

    # Tache 2 : Transformation Bronze -> Silver
    # Utilise spark-submit pour lancer le script de transformation
    silver_task = BashOperator(
        task_id="transform_bronze_to_silver",
        bash_command=(
            "spark-submit "
            "--master local[*] "
            "--conf spark.sql.shuffle.partitions=4 "
            f"{SPARK_SCRIPTS_PATH}/batch/silver_transformer.py"
        ),
    )

    # Tache 3 : Agregation Silver -> Gold
    gold_task = BashOperator(
        task_id="aggregate_silver_to_gold",
        bash_command=(
            "spark-submit "
            "--master local[*] "
            "--conf spark.sql.shuffle.partitions=4 "
            f"{SPARK_SCRIPTS_PATH}/batch/gold_aggregator.py"
        ),
    )

    # Tache 4 : Validation post-traitement
    validate_task = BashOperator(
        task_id="validate_gold_output",
        bash_command=(
            'echo "[validation] Verification de l\'existence des fichiers Gold..." && '
            "ls -la outputs/project/gold_v2/repo_activity/ && "
            "ls -la outputs/project/gold_v2/pagerank/ && "
            'echo "[validation] Toutes les tables Gold sont presentes."'
        ),
    )

    # -- Definition de l'ordre d'execution --
    start_task >> silver_task >> gold_task >> validate_task
