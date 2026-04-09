FROM python:3.11-slim
WORKDIR /app/backend

RUN apt-get update && apt-get install -y build-essential

COPY pyproject.toml .

RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -e .
RUN pip install --no-cache-dir debugpy
RUN playwright install --with-deps chromium

COPY . .

WORKDIR /app/
EXPOSE 5001

CMD ["python", "backend/app.py"]
