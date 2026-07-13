FROM python:3.12-slim

ARG HOST=0.0.0.0
ARG PORT=5000
ARG DB_USERNAME=postgres
ARG PASSWORD=postgres
ARG DATABASE=acadelytics
ARG DB_HOST=db
ARG ACCESS_TOKEN_SECRET=supersecret_jwt_key
ARG cookieKey=supersecret_cookie

RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY src/ ./src
COPY wait-for-db.sh ./
RUN chmod +x ./wait-for-db.sh && sed -i 's/\r$//' ./wait-for-db.sh && mkdir -p /app/src/config && if [ ! -f /app/src/config/.env ]; then printf 'HOST=%s\nPORT=%s\nDB_USERNAME=%s\nPASSWORD=%s\nDATABASE=%s\nDB_HOST=%s\nACCESS_TOKEN_SECRET=%s\ncookieKey=%s\n' "$HOST" "$PORT" "$DB_USERNAME" "$PASSWORD" "$DATABASE" "$DB_HOST" "$ACCESS_TOKEN_SECRET" "$cookieKey" > /app/src/config/.env; fi

ENV PYTHONUNBUFFERED=1 \
    HOST=$HOST \
    PORT=$PORT \
    DB_USERNAME=$DB_USERNAME \
    PASSWORD=$PASSWORD \
    DATABASE=$DATABASE \
    DB_HOST=$DB_HOST \
    ACCESS_TOKEN_SECRET=$ACCESS_TOKEN_SECRET \
    cookieKey=$cookieKey
EXPOSE 5000

WORKDIR /app/src
CMD ["sh", "/app/wait-for-db.sh"]
