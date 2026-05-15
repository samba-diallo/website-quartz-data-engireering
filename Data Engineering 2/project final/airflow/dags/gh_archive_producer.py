"""
DAG Airflow - Producer Kafka (GitHub Archive)
=============================================
Ce DAG declenche le Producer Python qui telecharge les fichiers
horaires de GitHub Archive et les envoie dans Kafka.

Il peut etre execute manuellement ou planifie pour ingerer
des heures specifiques via les parametres du DAG.

Auteur : Samba DIALLO
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# -- Configuration par defaut du DAG --
default_args = {
    "owner": "samba-diallo",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="gh_archive_kafka_producer",
    default_args=default_args,
    description="Ingestion des fichiers horaires GH Archive dans Kafka",
    schedule_interval=None,  # Declenchement manuel uniquement
    start_date=datetime(2025, 1, 15),
    catchup=False,
    max_active_runs=1,
    tags=["github-archive", "kafka", "ingestion"],
    # Parametres configurables lors du declenchement manuel
    params={
        "hours": "2025-01-15-10,2025-01-15-11,2025-01-15-12,2025-01-15-13",
    },
) as dag:

    # Tache unique : lancement du Producer avec les heures specifiees
    produce_task = BashOperator(
        task_id="run_kafka_producer",
        bash_command=(
            'echo "[producer] Demarrage de l\'ingestion Kafka..." && '
            "GH_ARCHIVE_HOURS={{ params.hours }} "
            "KAFKA_BOOTSTRAP_SERVERS=kafka:29092 "
            "python /opt/producer/gh_producer.py && "
            'echo "[producer] Ingestion terminee avec succes."'
        ),
    )

    produce_task
