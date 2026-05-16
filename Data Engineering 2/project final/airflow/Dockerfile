FROM apache/airflow:2.10.2

USER root

# Installation de Java (requis pour PySpark)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

# Etape 1 : Installation des dependances Python (PySpark, Kafka, Requests)
RUN pip install --no-cache-dir "pyspark==3.5.2" "kafka-python-ng" "requests"

# Etape 2 : Installation du provider Spark SANS ses dependances
# pour eviter que pip ne mette a jour Airflow vers la version 3.x
RUN pip install --no-cache-dir --no-deps "apache-airflow-providers-apache-spark==4.10.0"
