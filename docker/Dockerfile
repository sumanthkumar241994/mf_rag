FROM python:3.12-slim
WORKDIR app/

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/list/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY ingestion ./ingestion
COPY ecs_entrypoint.py .

CMD ["python", "ecs_entrypoint.py"]
