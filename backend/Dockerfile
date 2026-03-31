FROM python:3.11-slim
WORKDIR /app/backend
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir debugpy
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
