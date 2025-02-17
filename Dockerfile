FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt && \
	.venv/bin/pip install --upgrade numpy pandas

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["python", "app.py"]
