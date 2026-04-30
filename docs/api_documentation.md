# Phishing Detection API Reference Documentation

## Overview

This document describes the REST API exposed by the phishing detection backend. The API accepts URLs for analysis, returns phishing/safe verdicts based on the ML model,and provides access to historical scan records.

- **Base URL (local):** `http://localhost:5001`
- **Base URL (Docker):** `http://backend:5001`
- **Protocol:** HTTP/HTTPS
- **Data format:** JSON (except CSV export)
- **Authentication:** None, API is open/unauthenticated

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Conventions](#conventions)
3. [CORS Policy](#cors-policy)
4. [Endpoints](#endpoints)
   - [Health Check](#1-health-check)
   - [Scan a URL](#2-scan-a-url)
   - [List Scan History](#3-list-scan-history)
   - [Delete a Scan](#4-delete-a-scan)
   - [Export Scans as CSV](#5-export-scans-as-csv)
   - [Log an Error](#6-log-an-error)
5. [Data Models](#data-models)
6. [Error Reference](#error-reference)
7. [ML Model Details](#ml-model-details)
8. [Environment & Configuration](#environment--configuration)

---

## Quick Start

```bash
# 1. Check the server is running
curl http://localhost:5001/
# → Working!

# 2. Scan a URL for phishing
curl -X POST http://localhost:5001/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
# → {"is_safe": true, "confidence": 96.3200, "explanation": [...]}

# 3. Retrieve the 10 most recent scans
curl "http://localhost:5001/scans?limit=10&offset=0"

# 4. Download all scans as CSV
curl http://localhost:5001/scans/export -o scan_history.csv
```

---

## Conventions

| Convention | Detail |
|---|---|
| **Request body** | JSON object; set `Content-Type: application/json` |
| **Response body** | JSON object (or CSV for the export endpoint) |
| **Timestamps** | ISO 8601 UTC (e.g. `2024-03-15T10:30:00+00:00`) |
| **Confidence** | Float in the range `[0, 100]`, rounded to 4 decimal places |
| **Boolean fields** | JSON `true` / `false` (not `1` / `0` or `"true"` / `"false"`) |
| **Pagination** | `limit` + `offset` query parameters on list endpoints |

---

## CORS Policy

Cross-Origin requests are accepted from the following origins only:

```
http://127.0.0.1:80
http://127.0.0.1:6969
http://127.0.0.1:5173
http://localhost:5173
http://localhost:6969
```

Requests from any other origin will be rejected by the browser's CORS enforcement.

---

## API Endpoints

---

### 1. Health Check

Verify that the server is running and reachable.

```
GET /
```

#### Response

| Status | Body |
|---|---|
| `200 OK` | `Working!` (plain text) |

#### Example

```bash
curl http://localhost:5001/
```

```
Working!
```

---

### 2. URL Scan
Submit a URL for phishing analysis. The server validates the URL, runs it through the ML pipeline, persists the result anonymously, and returns a verdict with a confidence score and human-readable explanations.
```
POST /scan
Content-Type: application/json
```

#### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | The URL to analyse. If no scheme is present, `http://` is prepended automatically. Only `http` and `https` schemes are accepted. |

```json
{
  "url": "https://www.example.com"
}
```

#### URL Processing Pipeline

Before the URL reaches the ML model, the server applies the following transformations:

1. Leading/trailing whitespace is stripped.
2. If no URL scheme is present, `http://` is prepended.
3. The scheme is validated, and only `http` and `https` are allowed.
4. The domain and TLD are validated using `tldextract`. The URL must have both.
5. The path and query string are % encoded to neutralise XSS and SQL injection payloads.

#### Response: `200 OK`

```json
{
  "is_safe": true,
  "confidence": 96.3200,
  "explanation": [
    "does have title",
    "does not have obfuscated characters",
    "domain is short"
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `is_safe` | boolean | `true` if the URL is classified as safe; `false` if classified as phishing. |
| `confidence` | number | Probability (0–100) that the URL is **not** phishing, as determined by the model. |
| `explanation` | array of strings | Up to 3 human-readable feature explanations produced by the LIME explainer. If the URL matched the whitelist, this will be `["website found on whitelist"]`. |

#### Response: Errors

| Status | Condition | Error message |
|---|---|---|
| `400` | Request body is not JSON | `"Send JSON request"` |
| `400` | Request body is not a JSON object | `"Invalid request body"` |
| `400` | `url` field is missing or not a string | `"Missing/Invalid URL field"` |
| `400` | URL scheme is present but not `http` or `https` | `"Invalid URL scheme"` |
| `400` | URL has no recognisable domain or TLD | `"Invalid URL format"` |
| `400` | ML pipeline failed to produce a result | `"URL could not be scanned"` |

#### Examples

```bash
# Safe URL
curl -X POST http://localhost:5001/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

```json
{
  "is_safe": true,
  "confidence": 99.9900,
  "explanation": ["website found on whitelist"]
}
```

```bash
# URL without scheme (http:// prepended automatically)
curl -X POST http://localhost:5001/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "suspicious-login.xyz/paypal/verify"}'
```

```json
{
  "is_safe": false,
  "confidence": 8.4321,
  "explanation": [
    "does have submit button",
    "does not have copyright info",
    "u r l length is longer than usual"
  ]
}
```

```bash
# Invalid scheme
curl -X POST http://localhost:5001/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "ftp://files.example.com"}'
```

```json
{
  "error": "Invalid URL scheme"
}
```

---

### 3. List Scan History

Retrieve a paginated list of past scan records, ordered by most recent first. No user identification is stored, all scans are anonymous.

```
GET /scans
```

> **Legacy alias:** `POST /list_scans` maps to the same handler and accepts the same query parameters.

#### Query Parameters

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `limit` | integer | `100` | `1 – 500` | Maximum number of records to return. The server caps this at 500 regardless of the value supplied. |
| `offset` | integer | `0` | `>= 0` | Number of records to skip before returning results. Use with `limit` for pagination. |

#### Response: `200 OK`

```json
{
  "scans": [
    {
      "id": 42,
      "url": "https://www.example.com",
      "is_safe": true,
      "confidence": 96.3200,
      "scanned_at": "2024-03-15T10:30:00+00:00",
      "explanation": "does have title, does not have obfuscated characters"
    }
  ],
  "limit": 10,
  "offset": 0
}
```

| Field | Type | Description |
|---|---|---|
| `scans` | array | Ordered list of scan records (most recent first). |
| `scans[].id` | integer | Unique scan identifier (auto-incrementing). |
| `scans[].url` | string | The sanitised URL that was scanned. |
| `scans[].is_safe` | boolean | Model verdict. |
| `scans[].confidence` | number | Confidence score (0–100). |
| `scans[].scanned_at` | string | ISO 8601 UTC timestamp of when the scan was performed. |
| `scans[].explanation` | string | Comma-separated explanation strings. Empty string if none were stored. |
| `limit` | integer | The effective `limit` value used for this response. |
| `offset` | integer | The effective `offset` value used for this response. |

#### Response: Errors

| Status | Condition | Error message |
|---|---|---|
| `400` | `limit` or `offset` cannot be parsed as integers | `"limit and offset must be integers"` |
| `400` | `limit < 1` or `offset < 0` | `"limit must be >= 1 and offset must be >= 0"` |
| `500` | Database error | `"could not retrieve scan history"` |

#### Pagination Example

```bash
# Page 1: records 1–25
curl "http://localhost:5001/scans?limit=25&offset=0"

# Page 2: records 26–50
curl "http://localhost:5001/scans?limit=25&offset=25"

# Page 3: records 51–75
curl "http://localhost:5001/scans?limit=25&offset=50"
```

---

### 4. Delete a Scan

Permanently delete a single scan record by its ID.

```
DELETE /scans/<id>
```

#### Path Parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | The unique ID of the scan to delete. |

#### Response: `200 OK`

```json
{
  "deleted": 42
}
```

| Field | Type | Description |
|---|---|---|
| `deleted` | integer | The ID of the scan that was deleted. |

#### Response: Errors

| Status | Condition | Error message |
|---|---|---|
| `404` | No scan with the given ID exists | `"scan not found"` |

#### Example

```bash
curl -X DELETE http://localhost:5001/scans/42
```

```json
{
  "deleted": 42
}
```

---

### 5. Export Scans as CSV

Download all scan records (up to 10,000) as a CSV file. Useful for offline analysis or reporting.

```
GET /scans/export
```

#### Response: `200 OK`

| Header | Value |
|---|---|
| `Content-Type` | `text/csv` |
| `Content-Disposition` | `attachment; filename=scan_history.csv` |

The response body is a CSV document with the following columns:

| Column | Type | Description |
|---|---|---|
| `id` | integer | Scan ID |
| `url` | string | Scanned URL |
| `is_safe` | boolean | Model verdict |
| `confidence` | number | Confidence score (0–100) |
| `scanned_at` | string | ISO 8601 UTC timestamp |
| `explanation` | string | Comma-separated explanations |

```csv
id,url,is_safe,confidence,scanned_at,explanation
1,https://www.example.com,True,96.32,2024-03-15T10:30:00+00:00,"does have title, domain is short"
2,http://suspicious.xyz/login,False,11.45,2024-03-15T11:00:00+00:00,"does have submit button"
```

#### Response: Errors

| Status | Condition | Error message |
|---|---|---|
| `500` | Database error | `"could not retrieve scan history"` |

#### Example

```bash
# Download to file
curl http://localhost:5001/scans/export -o scan_history.csv

# Pipe into another tool
curl -s http://localhost:5001/scans/export | cut -d',' -f1,3,4
```

---

### 6. Log an Error

Submit an error or diagnostic message for server side logging. Intended for use by the frontend or other integrated clients.

```
POST /error
Content-Type: application/json
```

#### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `info` | string | Yes | The error message or contextual information to log. |
| `level` | string | No | Log severity level. Accepted values: `"ERROR"` (default), `"CRITICAL"`. |

```json
{
  "info": "Model prediction timed out for http://example.com",
  "level": "ERROR"
}
```

#### Log Files Written

| Level | File |
|---|---|
| `ERROR` | `logs/api_errors.txt` |
| `CRITICAL` | `logs/critical_failures.txt` |

Each line in the log file is a JSON object:

```json
{"timestamp": "2024-03-15T10:30:00.123456", "log_type": "ERROR", "message": "[127.0.0.1] Model prediction timed out for http://example.com"}
```

#### Response: `200 OK`

```json
true
```

#### Response: Errors

| Status | Condition | Error message |
|---|---|---|
| `400` | Request body is not a JSON object | `"Invalid request body"` |
| `400` | `info` field is missing or not a string | `"Empty information field"` |

#### Example

```bash
curl -X POST http://localhost:5001/error \
  -H "Content-Type: application/json" \
  -d '{"info": "Unexpected null response from ML pipeline", "level": "CRITICAL"}'
```

```json
true
```

---

## Data Models

### Scan Object

Returned by `GET /scans` within the `scans` array.

```json
{
  "id": 42,
  "url": "https://www.example.com/path?query=value",
  "is_safe": true,
  "confidence": 96.3200,
  "scanned_at": "2024-03-15T10:30:00+00:00",
  "explanation": "does have title, does not have obfuscated characters"
}
```

### Scan Result Object

Returned directly by `POST /scan`.

```json
{
  "is_safe": false,
  "confidence": 8.4321,
  "explanation": [
    "does have submit button",
    "does not have copyright info",
    "u r l length is longer than usual"
  ]
}
```

> Note: `explanation` is an **array of strings** in the scan result, but a **comma-separated string** in the scan history list. This reflects the storage format in the database.

### Error Object

Returned by all endpoints on failure.

```json
{
  "error": "descriptive error message"
}
```

---

## Error Reference

Complete list of all error responses across all endpoints.

| HTTP Status | Error message | Endpoint(s) | Cause |
|---|---|---|---|
| `400` | `"Send JSON request"` | `POST /scan` | Missing or incorrect `Content-Type` header |
| `400` | `"Invalid request body"` | `POST /scan`, `POST /error` | Body is not a JSON object (e.g. array, primitive) |
| `400` | `"Missing/Invalid URL field"` | `POST /scan` | `url` key absent or not a string |
| `400` | `"Invalid URL scheme"` | `POST /scan` | Scheme present but not `http` or `https` |
| `400` | `"Invalid URL format"` | `POST /scan` | No recognisable domain or TLD |
| `400` | `"URL could not be scanned"` | `POST /scan` | ML pipeline returned `None` or threw an exception |
| `400` | `"limit and offset must be integers"` | `GET /scans` | Non-integer value supplied for `limit` or `offset` |
| `400` | `"limit must be >= 1 and offset must be >= 0"` | `GET /scans` | `limit < 1` or `offset < 0` |
| `400` | `"Empty information field"` | `POST /error` | `info` field missing or not a string |
| `404` | `"scan not found"` | `DELETE /scans/<id>` | No record exists with the given ID |
| `500` | `"could not retrieve scan history"` | `GET /scans`, `GET /scans/export` | Database query failed |

---

## ML Model Details

### Pipeline Summary

When a URL is submitted to `POST /scan`, the ML pipeline performs the following steps:

1. **Whitelist check**: the domain is compared against a list of the top 100,000 trusted domains. On an exact match, the pipeline ends early and automatically returns `is_safe=true, confidence=100, explanation=["website found on whitelist"]`.
2. **Feature extraction**: 32+ features are extracted from the URL structure and the page's HTML content.
3. **Classification**: a pre-trained logistic regression model produces a binary verdict and a confidence probability.
4. **Explanation**: the LIME (Local Interpretable Model-agnostic Explanations) framework identifies the top 3 features that most influenced the prediction, which are converted to human readable strings.

### Feature Categories

| Category | Example Features |
|---|---|
| URL structure | URL length, domain length, TLD length, number of subdomains, HTTPS, digit ratio, special character ratio, obfuscation indicators |
| Domain similarity | Levenshtein distance, Jaro-Winkler similarity, and LCS against whitelist entries |
| HTML content | Page line count, presence of title/favicon/submit button/copyright/social links, number of JS includes, external vs self referencing links, financial keywords |

### Confidence Interpretation

| `confidence` range | Suggested interpretation |
|---|---|
| `90 – 100` | Very likely safe |
| `60 – 89` | Probably safe |
| `40 – 59` | Uncertain, treat with caution |
| `10 – 39` | Probably phishing |
| `0 – 9` | Very likely phishing |

The confidence value represents the model's estimated probability that the URL is **not phishing**.

### Explanation String Format

LIME feature names are converted from PascalCase to readable sentences:

| Raw feature condition | Human-readable explanation |
|---|---|
| `HasTitle <= 0` | `"does not have title"` |
| `HasTitle > 0` | `"does have title"` |
| `HasFavicon > 0` | `"does have favicon"` |
| `NoOfSubDomain >= 3` | `"no of sub domain is longer/bigger than usual"` |
| `0.5 <= URLTitleMatchScore <= 99.5` | `"u r l title match score is between 0.5 and 99.5"` |

---

## Environment & Configuration

### Database Connection

The backend connects to a PostgreSQL database. Configuration is supplied via environment variables:

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `phishing_db` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | *(empty)* | Database password |
| `DB_CONNECT_TIMEOUT` | `5` | Connection timeout in seconds |

### Database Schema

```sql
CREATE TABLE IF NOT EXISTS scans (
    id          SERIAL PRIMARY KEY,
    url         TEXT        NOT NULL,
    is_safe     BOOLEAN     NOT NULL,
    confidence  NUMERIC     NOT NULL CHECK (confidence >= 0 AND confidence <= 100),
    scanned_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    explanation TEXT
);
```

### Running the Server

**Directly:**

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=phishing_db
export DB_USER=postgres
export DB_PASSWORD=yourpassword

cd backend
python app.py
# Server starts on http://0.0.0.0:5001
```

**Via Docker Compose:**

```bash
docker compose up --build
# Backend: http://localhost:5001
# Frontend: http://localhost:6969
# PostgreSQL: localhost:5433
```

### Log Files

| File | Contents |
|---|---|
| `logs/app.txt` | All incoming requests (INFO level) |
| `logs/api_errors.txt` | Client errors (400 level) and warnings |
| `logs/critical_failures.txt` | Uncaught exceptions and critical failures |
| `logs/preprocessor_errors.txt` | ML feature extraction failures |

---
