# Installation and Operational Manual

Within our development team there are two ways of running the model.

Docker being the most portable but the most annoying, slowest and finicky to debug is the perferred method accoridng to the university.

## Repository file structure (high level)

```
.
├── docker-compose.yml
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── pyproject.toml
│   └── ml/
│       ├── pipeline.py
│       └── preprocessor.py
└── frontend/
  ├── package.json
  ├── vite.config.js
  └── src/
    ├── api.ts
    ├── App.tsx
    └── main.tsx
```

Anything else beyond these files are considered configuration, test files, research or documentation files.

For example in the backend, machine learning research and dataset is labelled as the `ml` folder.


## High level files required to run the servers

### Backend server (Flask)

- [backend/app.py](backend/app.py): entrypoint for the Flask API server.
- [backend/pyproject.toml](backend/pyproject.toml): backend dependencies and packaging.
- [backend/database.py](backend/database.py): database configuration and connection helpers.
- [backend/ml/pipeline.py](backend/ml/pipeline.py): model inference pipeline used by the API.
- [backend/ml/preprocessor.py](backend/ml/preprocessor.py): feature extraction for URL scans.

### Frontend server (Vite + React)

- [frontend/package.json](frontend/package.json): npm scripts and frontend dependencies.
- [frontend/vite.config.js](frontend/vite.config.js): Vite dev server and build config.
- [frontend/src/main.tsx](frontend/src/main.tsx): app bootstrap and React root.
- [frontend/src/App.tsx](frontend/src/App.tsx): main app component.
- [frontend/src/api.ts](frontend/src/api.ts): API client for backend requests.

## Run with Docker (recommended)

To run with docker, we suggest to start at the root repository directory

```bash
docker compose up --build
```


Services:
- Frontend: http://localhost:6969
- Backend API: http://localhost:5001
- Postgres: localhost:5433

Note that the dockerfile will automatically


Run the test container (optional):


```bash
docker compose --profile debug up --build test
```

### Running tests within docker

#### Run test cases

```bash
docker compose -f 'docker-compose.yml' up -d --build 'test'
```



## Running locally

Running locally confers advantages such as easier debug time or long term stability on a server.

### 1) Start Postgres


If you do not already have Postgres running locally, it is easier start to the DB docker container and point the backend to it:


```bash
docker compose up -d db
```

rather than installing PostgresSQL

### 2) Backend API (Flask)


From the repo root:


```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e backend
python -m playwright install --with-deps chromium



export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=phishing_db
export DB_USER=postgres
export DB_PASSWORD=postgres

python backend/app.py
```
The API listens on http://localhost:5001


### 3) Frontend (Vite)


```bash
cd frontend
npm install
npm run dev
```



## Run Test cases:

### 1) To run backend tests

Change directory into the repository root.
```bash
python -m pip install pytest-cov
python -m pytest
```

and expect to observe this:
```bash
 python -m pytest

========================================================= test session starts =========================================================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/khalifa/capstone-project-26t1-3900-m18b-date
plugins: cov-7.1.0, dash-4.0.0
collected 13 items

test/ai_test.py .                                                                                                               [  7%]
test/backend_test.py ............                                                                                               [100%]

========================================================= 13 passed in 34.31s =========================================================

```

#### 1b) To run with code coverage:

```bash
python -m pytest --cov=backend --cov-report=term-missing
```

Note this test case covers for system code for the backend only. Not research code


### 2) To run frontend tests

Change directory into the repository root.

```bash
cd frontend
npm run test
```

and you should expect to see something like this:

```bash
npm run test --coverage

> phishing-checker@0.0.0 test
> vitest


 DEV  v3.2.4 /home/khalifa/capstone-project-26t1-3900-m18b-date/frontend

 ✓ src/tests/api.test.ts (2 tests) 4ms
 ✓ src/tests/App.test.tsx (1 test) 15ms
stdout | src/tests/Homepage.test.tsx > HomePage Logic > triggers the scanURL API call on submit
{ is_safe: true, confidence: 0.99 }

stdout | src/tests/Homepage.test.tsx > HomePage Logic > renders 'Verified' when API returns safe
{ is_safe: true }

 ✓ src/tests/Homepage.test.tsx (3 tests) 609ms
   ✓ HomePage Logic > renders 'Verified' when API returns safe  523ms
 ✓ src/tests/HistoricData.test.tsx (2 tests) 262ms

```

#### 2b) To run with code coverage:

TODO: @ccyra-unsw @caitlindang @Shadz11
```bash
npm run coverage
```

### Troubleshooting common issues or warnings

1) According to some developers, sometimes the docker database would not work.

Solution: Please delete the volume for the pgdata of the docker container

2) The docker port is being blocked and cannot run

Solution: Some developers with may have their prots reserved. Please check that port 5001, 5433 or 696 are free

3) The URL scanning sometimes takes long:

Solution: This is normal particularly for sites that are overseas because the HTML fetch engine uses 4 heuristics to determine if the webpage is either dynamically or statically loaded throught a series of checks.

4) There are several warning messages when the URL scan occurs:

Solution: This is because the HTML fetch engine utilises the Playwright library and the exception does not occur within our codebase when the website or URL bypasses the checks
