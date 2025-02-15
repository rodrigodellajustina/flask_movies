FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

# Criar ambiente virtual e instalar dependências
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Definir o PATH para usar o ambiente virtual
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["python", "app.py"]