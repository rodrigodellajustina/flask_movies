FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    libatlas-base-dev \
    gfortran \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

# Cria o ambiente virtual e instala as dependências
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt && \
    .venv/bin/pip install --no-cache-dir --force-reinstall numpy

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["python", "app.py"]
