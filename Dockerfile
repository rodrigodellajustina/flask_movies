FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# Atualiza PIP Instalar dependências
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]