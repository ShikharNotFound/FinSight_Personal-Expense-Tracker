FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PROJECT_ROOT=/app
ENV TRANSACTION_WORKSPACE_DIR=/tmp/finsight-transactions
ENV IMAGES_DIR=/tmp/finsight-transactions/images
ENV OUTPUTS_DIR=/tmp/finsight-transactions/output
ENV SCRIPTS_DIR=/app/scripts

RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ["Transactions/code1 copy 2/requirements.txt", "/app/transaction-requirements.txt"]
RUN pip install --no-cache-dir -r /app/transaction-requirements.txt

COPY ["Transactions/code1 copy 2", "/app/transaction_service"]
COPY ["scripts", "/app/scripts"]

RUN mkdir -p /tmp/finsight-transactions/images /tmp/finsight-transactions/output

WORKDIR /app/transaction_service

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
