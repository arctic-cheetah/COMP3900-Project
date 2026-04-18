-- DETERMINE IF THIS NEEDED IF RUNNING IN DOCKER ONLY
-- DROP TABLE IF EXISTS scans;

CREATE TABLE IF NOT EXISTS scans (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    is_safe BOOLEAN NOT NULL,
    confidence NUMERIC NOT NULL CHECK (
        confidence >= 0
        AND confidence <= 100
    ),
    scanned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), 
    explanation TEXT
);
