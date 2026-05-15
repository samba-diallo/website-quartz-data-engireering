# ============================================
# Dockerfile - Producer Kafka (GitHub Archive)
# ============================================
FROM python:3.10-slim

WORKDIR /app

# Installation des dependances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Lancement du producer
CMD ["python", "-u", "gh_producer.py"]
