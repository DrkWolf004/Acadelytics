FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY src/ ./src
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
WORKDIR /app/src
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
