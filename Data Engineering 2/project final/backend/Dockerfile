FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (Render injecte $PORT au runtime ; 8000 par défaut en local)
EXPOSE 8000

# Run the API — forme shell pour substituer $PORT (sinon non interpolé)
CMD python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
