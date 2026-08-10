# COMP3900 Project

Phishing and spam detection project for COMP3900. The application provides a web UI and a Flask API for scanning URLs, classifying them as safe or suspicious, and storing scan history.

## Overview

The repository contains three main parts:

- `frontend/`: Vite + React client for URL submission and viewing scan history.
- `backend/`: Flask API, PostgreSQL integration, and model orchestration.
- `ml/`: feature extraction, preprocessing, and model pipeline code.

## Tech Stack

- Frontend: React, TypeScript, Vite
- Backend: Flask, Flask-CORS, psycopg2
- Database: PostgreSQL 16
- ML/Data: scikit-learn, pandas, joblib, tldextract
- Containers: Docker Compose

## Repository Structure

```text
.
|-- backend/
|   |-- app.py
|   |-- database.py
|   |-- schema.sql
|   `-- pyproject.toml
|-- frontend/
|   |-- src/
|   `-- package.json
|-- ml/
|   |-- pipeline.py
|   |-- preprocessor.py
|   `-- data/
|-- test/
|   |-- backend_test.py
|   `-- ai_test.py
`-- docker-compose.yml
```

## Prerequisites

For Docker-based development:

- Docker
- Docker Compose

For local development:

- Python 3.11+
- Node.js 18+
- npm
- PostgreSQL

## Quick Start With Docker

This is the most portable way to run the full stack.

```bash
docker pull nginx:alpine
docker compose up --build
```

Services exposed by Docker Compose:

- Frontend: `http://localhost:6969`
- Backend API: `http://localhost:5001`
- PostgreSQL: `localhost:5433`

To stop the stack:

```bash
docker compose down
```

To remove containers and volumes:

```bash
docker compose down -v
```

## Local Development

### 1. Start PostgreSQL

You can use your own PostgreSQL instance or reuse the database container only:

```bash
docker compose up -d db
```

The default database configuration used by Docker Compose is:

- Host: `localhost`
- Port: `5433`
- Database: `phishing_db`
- User: `postgres`
- Password: `postgres`

### 2. Start the Backend

Install backend dependencies from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./backend
playwright install --with-deps chromium
```

Export database settings if you are using the Docker database on port `5433`:

```bash
export DB_HOST=localhost
export DB_PORT=5433
export DB_NAME=phishing_db
export DB_USER=postgres
export DB_PASSWORD=postgres
```

Run the backend from the repository root:

```bash
python backend/app.py
```

The API will be available at `http://localhost:5001`.

### 3. Start the Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

By default, the frontend expects the backend at `http://localhost:5001`.

If needed, you can override that with a Vite environment variable:

```bash
VITE_API_URL=http://localhost:5001 npm run dev
```

## API

### Health Check

```http
GET /
```

Returns:

```text
Working!
```

### Scan a URL

```http
POST /scan
Content-Type: application/json
```

Request body:

```json
{
    "url": "https://example.com"
}
```

Successful response:

```json
{
    "is_safe": true,
    "confidence": 0.97,
    "explanation": []
}
```

### List Saved Scans

```http
GET /scans?limit=100&offset=0
```

There is also a legacy route used by the current frontend:

```http
POST /list_scans
```

### Delete a Saved Scan

```http
DELETE /scans/<scan_id>
```

### Export Scan History

```http
GET /scans/export
```

Returns a CSV file named `scan_history.csv`.

### Log an Error

```http
POST /error
Content-Type: application/json
```

Request body:

```json
{
    "info": "error details",
    "level": "ERROR"
}
```

## Running Tests

### Integration Tests With Docker

The `test` service is attached to the `debug` profile:

```bash
docker compose --profile debug up --build test
```

### Local Test Run

From the repository root:

```bash
pytest test/
```

Note: the backend integration tests expect the API to be reachable at `http://127.0.0.1:5001` unless `BACKEND_URL` is set.

## Data and Model References

The ML pipeline uses phishing URL datasets stored under `ml/data/`.

- Research paper: [linkinghub.elsevier.com/retrieve/pii/S0167404823004558](https://linkinghub.elsevier.com/retrieve/pii/S0167404823004558)
- Dataset source: [archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)

## Logs

Runtime logs are written to the `logs/` directory. The backend also creates log files such as:

- `logs/app.txt`
- `logs/api_errors.txt`
- `logs/critical_failures.txt`

## Contributing

Pull requests are welcome. For larger changes, open an issue first so the scope and approach can be discussed before implementation.

When contributing:

- keep changes focused
- add or update tests where appropriate
- preserve the existing project structure and conventions

## Authors

Joules, Ray, Kelly, Lara, Shadab, Caitlin

## License

[MIT](https://choosealicense.com/licenses/mit/)
