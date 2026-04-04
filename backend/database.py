import os
import sys
import logging
import psycopg2
import datetime
import psycopg2.extras
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432)),
    "dbname": os.environ.get("DB_NAME", "phishing_db"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "connect_timeout": 5,
}


# Open and return a new psycopg2 connection
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@contextmanager
def get_cursor():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as c:
            yield c
            conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


# Initialise database by running schema.sql if scans table does not already exist
def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
    except FileNotFoundError:
        logger.critical("schema.sql not found at %s, cannot initialise DB", schema_path)
        sys.exit(1)

    try:
        with get_cursor() as cur:
            cur.execute(schema_sql)
        logger.info("Database initialised successfully.")
    except psycopg2.OperationalError as e:
        logger.critical("Could not connect to PostgreSQL: %s", e)
        sys.exit(1)


# Persist an anonymous scan result to the scans table
def save_scan(url: str, is_safe: bool, confidence: float):
    query = """
        INSERT INTO scans (url, is_safe, confidence)
        VALUES (%s, %s, %s)
        RETURNING id, scanned_at;
    """

    try:
        with get_cursor() as cur:
            cur.execute(query, (url, is_safe, round(confidence, 4)))
            row = cur.fetchone()
            scan_id = row["id"] if row else None
            logger.info(
                "Scan saved — id=%s is_safe=%s confidence=%.4f",
                scan_id,
                is_safe,
                confidence,
            )
            return scan_id
    except Exception as e:
        logger.error("Failed to save scan: %s", e)
        return None


# Retrieves paginated scan history with the most recent first
def get_all_scans(limit: int = 500, offset: int = 0):

    # server side cap to prevent abuse from frontend
    limit = min(limit, 500)
    query = """
        SELECT id, url, is_safe, confidence, scanned_at
        FROM scans
        ORDER BY scanned_at DESC
        LIMIT %s OFFSET %s;
    """
    try:
        with get_cursor() as cur:
            cur.execute(query, (limit, offset))
            rows = cur.fetchall()
            return [
                {
                    "id": row["id"],
                    "url": row["url"],
                    "is_safe": row["is_safe"],
                    "confidence": float(row["confidence"]),
                    "scanned_at": row["scanned_at"].isoformat(),
                }
                for row in rows
            ]

    except Exception as e:
        logger.error("Unable to retrieve scans: %s", e)
        return None
