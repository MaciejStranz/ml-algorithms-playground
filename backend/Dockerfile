FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /tmp/backend-requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /tmp/backend-requirements.txt

COPY ml_core /app/ml_core
RUN pip install -e /app/ml_core

COPY backend /app/backend
RUN chmod +x /app/backend/entrypoint.sh

WORKDIR /app/backend


EXPOSE 8000

ENTRYPOINT ["/app/backend/entrypoint.sh"]

