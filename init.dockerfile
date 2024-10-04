FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /app /app
COPY .env /app/.env
COPY /data/questions.json /app
COPY /grafana /app
EXPOSE 8501
CMD ["python", "-m", "app_init"]