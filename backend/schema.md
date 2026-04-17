# Database Schema

## Summary
The database stores all scan results anonymously. No user-identifying information (IP address, session ID, user account) is recorded.

## `scans` Table

| Column     | Type        | Constraint                          | Details                                              |
|------------|-------------|-------------------------------------|------------------------------------------------------|
| id         | SERIAL      | PRIMARY KEY                         | Unique scan identifier                               |
| url        | TEXT        | NOT NULL                            | Sanitised URL submitted for scanning                 |
| is_safe    | BOOLEAN     | NOT NULL                            | Model result: true = safe, false = phishing          |
| confidence | NUMERIC     | NOT NULL, CHECK (0 <= value <= 100) | Model confidence score rounded to 4dp                |
| scanned_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW()             | UTC timestamp of when the scan was recorded          |

## API Endpoints

| Method | Route           | Description                                                                       |
|--------|-----------------|-----------------------------------------------------------------------------------|
| POST   | `/scan`         | Run a URL through the model, saves result, returns is_safe + confidence           |
| GET    | `/scans`        | Paginated scan history. Query params: `limit` (default 100), `offset` (default 0) |
| POST   | `/list_scans`   | Alias for `GET /scans` (legacy)                                                   |
| DELETE | `/scans/<id>`   | Delete a scan by ID. Returns 404 if not found                                     |
| GET    | `/scans/export` | Download full scan history as a CSV file                                          |

## `database.py` Functions

| Function                              | Description                                                                              |
|---------------------------------------|------------------------------------------------------------------------------------------|
| `init_db()`                           | Runs `schema.sql` on startup to create the table if it does not exist, exits on failure. |
| `save_scan(url, is_safe, confidence)` | Inserts a scan row, returns the new `id`                                                 |
| `get_all_scans(limit, offset)`        | Returns scans ordered by most recent first, with server side cap of 500/request.         |
| `delete_scan(scan_id)`                | Deletes by ID, returns `True` if deleted, `False` if not found                           |

## Setup
1. Create the database: `createdb phishing_db`
2. Run the schema: `psql -d phishing_db -f schema.sql`
3. Set environment variables before starting the app:
```
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=phishing_db
export DB_USER=postgres
export DB_PASSWORD=yourpassword
```

## Dependencies
`psycopg2-binary`
