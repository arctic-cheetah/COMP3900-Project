FROM python:3.11-slim
WORKDIR /app/backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir debugpy
RUN playwright install --with-deps chromium
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
