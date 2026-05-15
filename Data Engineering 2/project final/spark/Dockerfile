FROM python:3.10-slim

# Installation de Java (requis pour PySpark) et procps (requis par Spark pour gerer ses processus)
RUN apt-get update && \
    apt-get install -y default-jre procps && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java

WORKDIR /app

# Installation de PySpark
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des scripts Spark
COPY . /app/spark/

# Par defaut, on lance le consumer Bronze streaming
CMD ["python", "-u", "/app/spark/streaming/bronze_consumer.py"]
