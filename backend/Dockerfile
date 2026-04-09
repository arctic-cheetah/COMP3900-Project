FROM python:3.11-slim

WORKDIR /app/backend

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -e .
RUN pip install --no-cache-dir debugpy

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
