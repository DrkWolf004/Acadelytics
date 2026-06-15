FROM python:3.12-slim

# Instalar netcat para verificar conectividad a PostgreSQL
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY src/ ./src
COPY wait-for-db.sh ./
RUN chmod +x ./wait-for-db.sh && sed -i 's/\r$//' ./wait-for-db.sh

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

WORKDIR /app/src
CMD ["sh", "/app/wait-for-db.sh"]
