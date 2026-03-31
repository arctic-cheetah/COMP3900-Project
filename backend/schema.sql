CREATE TABLE IF NOT EXISTS scans (
    id          SERIAL          PRIMARY KEY,
    url         TEXT            NOT NULL,
    is_safe     BOOLEAN         NOT NULL,
    confidence  NUMERIC(6, 4)   NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    scanned_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);
 