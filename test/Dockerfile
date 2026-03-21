FROM python:3.11-slim
WORKDIR /app/test
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend_test.py ./
CMD ["pytest"]