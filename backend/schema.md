# Database Schema 
## Summary
The database stores all scan results anonymously, and no user identifying information (IP address, session ID, user account) is recorded

## `scans` Table
The `scans` table stores every URL scan in the following format:

| Column      | Type           | Constraint                                  | Details                                              |
|-------------|----------------|---------------------------------------------|------------------------------------------------------|
| id          | SERIAL         | PRIMARY KEY                                 | Auto incrementing unique scan identifier             |
| url         | TEXT           | NOT NULL                                    | The sanitised URL that was submitted for scanning    |
| is_safe     | BOOLEAN        | NOT NULL                                    | Model outcome: true = safe, false = phishing         |
| confidence  | NUMERIC(5, 4)  | NOT NULL, CHECK (value BETWEEN 0.0 AND 1.0) | Model confidence score (eg. 0.9731)                  |
| scanned_at  | TIMESTAMPTZ    | NOT NULL, DEFAULT NOW()                     | UTC timestamp of when the scan was recorded          |

## Setup
1. Create the database: `createdb phishing_db`
2. Run the schema: `psql -d phishing_db -f schema.sql`
3. Set environment variables before starting the webapp:
```
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=phishing_db
export DB_USER=postgres
export DB_PASSWORD=yourpassword
```

### Dependencies
`psycopg2-binary`