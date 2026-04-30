# Unit tests for backend helper functions + API routes, runs without a live server or DB, mocked external dependencies
import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock
from contextlib import contextmanager
import datetime
import psycopg2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import app as app_module
from app import app as flask_app, check_valid_url, sanitise_url, write_log


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# Check valid URL
def test_check_valid_url_http():
    assert check_valid_url("http://example.com") is True

def test_check_valid_url_https():
    assert check_valid_url("https://www.google.com") is True

def test_check_valid_url_empty_string():
    assert check_valid_url("") is False

def test_check_valid_url_none():
    assert check_valid_url(None) is False

def test_check_valid_url_non_string():
    assert check_valid_url(123) is False

def test_check_valid_url_no_tld():
    assert check_valid_url("notaurl") is False


# Sanitise URL
def test_sanitise_url_strips_whitespace():
    assert sanitise_url("  http://example.com  ") == "http://example.com"

def test_sanitise_url_encodes_xss_in_path():
    result = sanitise_url("http://example.com/<script>alert(1)</script>")
    assert "<script>" not in result

def test_sanitise_url_encodes_query_special_chars():
    result = sanitise_url("http://example.com/?q=<evil>")
    assert "<evil>" not in result

def test_sanitise_url_clean_url_unchanged():
    url = "http://example.com/path/to/page"
    assert sanitise_url(url) == url


# Write Log
def test_write_log_error_goes_to_error_file(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "ERROR_LOG", tmp_path / "errors.txt")
    monkeypatch.setattr(app_module, "CRITICAL_LOG", tmp_path / "critical.txt")
    write_log("something broke", "ERROR")
    entry = json.loads((tmp_path / "errors.txt").read_text().strip())
    assert entry["log_type"] == "ERROR"
    assert entry["message"] == "something broke"
    assert "timestamp" in entry

def test_write_log_critical_goes_to_critical_file(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "ERROR_LOG", tmp_path / "errors.txt")
    monkeypatch.setattr(app_module, "CRITICAL_LOG", tmp_path / "critical.txt")
    write_log("critical failure", "CRITICAL")
    entry = json.loads((tmp_path / "critical.txt").read_text().strip())
    assert entry["log_type"] == "CRITICAL"
    assert entry["message"] == "critical failure"


# Scan Route (mocked pipeline, DB)
def test_scan_pipeline_returns_none_gives_400(client):
    with patch("app.model_pipeline", return_value=None):
        res = client.post("/scan", json={"url": "http://example.com"})
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_scan_pipeline_success_returns_result(client):
    with patch("app.model_pipeline", return_value=(1, 95.0, ["domain is short"])):
        with patch("app.save_scan", return_value=1):
            res = client.post("/scan", json={"url": "http://example.com"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["is_safe"] is True
    assert data["confidence"] == 95.0
    assert "explanation" in data

def test_scan_non_json_body_returns_400(client):
    res = client.post("/scan", data="not json", content_type="text/plain")
    assert res.status_code == 400

def test_scan_missing_url_field_returns_400(client):
    res = client.post("/scan", json={"link": "http://example.com"})
    assert res.status_code == 400

def test_scan_invalid_scheme_ftp_returns_400(client):
    res = client.post("/scan", json={"url": "ftp://example.com"})
    assert res.status_code == 400

def test_scan_empty_url_returns_400(client):
    res = client.post("/scan", json={"url": ""})
    assert res.status_code == 400

def test_scan_url_non_string_returns_400(client):
    res = client.post("/scan", json={"url": 12345})
    assert res.status_code == 400


# Error route
def test_error_route_happy_path_returns_200(client):
    with patch("app.write_log"):
        res = client.post("/error", json={"info": "test error message", "level": "ERROR"})
    assert res.status_code == 200

def test_error_route_missing_info_returns_400(client):
    res = client.post("/error", json={"level": "ERROR"})
    assert res.status_code == 400

def test_error_route_non_json_returns_400(client):
    res = client.post("/error", data="not json", content_type="text/plain")
    assert res.status_code in (400, 415)

# ===== ADDITIONAL APP.PY COVERAGE =====

# write_log - open failure is silenced (lines 59-60)
def test_write_log_open_failure_is_silenced(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "ERROR_LOG", tmp_path / "nodir" / "errors.txt")
    write_log("test", "ERROR")  # directory doesn't exist, should not raise


# check_valid_url - tldextract raises returns False (lines 82-83)
def test_check_valid_url_tldextract_raises_returns_false():
    with patch("app.tldextract.extract", side_effect=Exception("parse error")):
        assert check_valid_url("http://example.com") is False

def test_health_check_returns_200(client):
    res = client.get("/")
    assert res.status_code == 200

def test_scan_json_array_body_returns_400(client):
    res = client.post("/scan", json=[1, 2, 3])
    assert res.status_code == 400

def test_scan_no_scheme_prepends_http(client):
    with patch("app.model_pipeline", return_value=(1, 90.0, ["ok"])):
        with patch("app.save_scan", return_value=1):
            res = client.post("/scan", json={"url": "example.com"})
    assert res.status_code == 200

def test_list_scans_success(client):
    with patch("app.get_all_scans", return_value=[]):
        res = client.get("/scans")
    assert res.status_code == 200
    data = res.get_json()
    assert "scans" in data

def test_list_scans_invalid_limit_returns_400(client):
    res = client.get("/scans?limit=abc")
    assert res.status_code == 400

def test_list_scans_limit_zero_returns_400(client):
    res = client.get("/scans?limit=0")
    assert res.status_code == 400

def test_list_scans_negative_offset_returns_400(client):
    res = client.get("/scans?offset=-1")
    assert res.status_code == 400

def test_list_scans_db_error_returns_500(client):
    with patch("app.get_all_scans", return_value=None):
        res = client.get("/scans")
    assert res.status_code == 500


# GET /scans - pagination params passed through
def test_list_scans_pagination_params(client):
    with patch("app.get_all_scans", return_value=[]):
        res = client.get("/scans?limit=10&offset=5")
    assert res.status_code == 200
    data = res.get_json()
    assert data["limit"] == 10
    assert data["offset"] == 5

def test_error_route_json_array_body_returns_400(client):
    res = client.post(
        "/error",
        data=json.dumps([1, 2, 3]),
        content_type="application/json",
    )
    assert res.status_code == 400


# DELETE /scans/<id> - success (lines 263-267)
def test_remove_scan_success(client):
    with patch("app.delete_scan", return_value=True):
        res = client.delete("/scans/1")
    assert res.status_code == 200
    assert res.get_json()["deleted"] == 1

def test_remove_scan_not_found(client):
    with patch("app.delete_scan", return_value=False):
        res = client.delete("/scans/999")
    assert res.status_code == 404

def test_export_scans_success(client):
    mock_scans = [
        {
            "id": 1,
            "url": "http://example.com",
            "is_safe": True,
            "confidence": 95.0,
            "scanned_at": "2024-01-01T00:00:00",
            "explanation": "safe",
        }
    ]
    with patch("app.get_all_scans", return_value=mock_scans):
        res = client.get("/scans/export")
    assert res.status_code == 200
    assert b"example.com" in res.data

def test_export_scans_db_error_returns_500(client):
    with patch("app.get_all_scans", return_value=None):
        res = client.get("/scans/export")
    assert res.status_code == 500

# DATABASE TESTS
import database as db_module
from database import init_db, save_scan, get_all_scans, delete_scan


def _cursor_ctx(mock_cur):
    @contextmanager
    def _cm():
        yield mock_cur
    return _cm


# get_connection
def test_get_connection_calls_psycopg2():
    with patch("database.psycopg2.connect") as mock_connect:
        mock_connect.return_value = MagicMock()
        db_module.get_connection()
        mock_connect.assert_called_once()

def test_get_cursor_commits_and_closes():
    mock_cur = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    with patch("database.get_connection", return_value=mock_conn):
        with db_module.get_cursor():
            pass
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


# get_cursor - exception triggers rollback
def test_get_cursor_exception_triggers_rollback():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=MagicMock())
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    with patch("database.get_connection", return_value=mock_conn):
        with pytest.raises(RuntimeError):
            with db_module.get_cursor():
                raise RuntimeError("boom")
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()

def test_init_db_success(tmp_path):
    schema = tmp_path / "schema.sql"
    schema.write_text("CREATE TABLE IF NOT EXISTS scans ();")
    mock_cur = MagicMock()
    with patch("database.os.path.join", return_value=str(schema)):
        with patch("database.get_cursor", _cursor_ctx(mock_cur)):
            init_db()
    mock_cur.execute.assert_called_once()

def test_init_db_schema_not_found():
    with patch("database.os.path.join", return_value="/yapyap/schema.sql"):
        with pytest.raises(SystemExit):
            init_db()


# init_db - DB connection error
def test_init_db_db_connection_error(tmp_path):
    schema = tmp_path / "schema.sql"
    schema.write_text("CREATE TABLE IF NOT EXISTS scans ();")
    with patch("database.os.path.join", return_value=str(schema)):
        with patch("database.get_cursor", side_effect=psycopg2.OperationalError("no db")):
            with pytest.raises(SystemExit):
                init_db()

def test_save_scan_returns_id():
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = {"id": 42}
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = save_scan("http://example.com", True, 95.0, ["safe site"])
    assert result == 42

def test_save_scan_no_explanation():
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = {"id": 1}
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = save_scan("http://example.com", False, 80.0)
    assert result == 1

def test_save_scan_no_row_returned():
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = None
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = save_scan("http://example.com", True, 90.0)
    assert result is None

def test_save_scan_exception_returns_none():
    with patch("database.get_cursor", side_effect=Exception("db error")):
        result = save_scan("http://example.com", True, 90.0)
    assert result is None

def test_get_all_scans_returns_rows():
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = [
        {
            "id": 1,
            "url": "http://example.com",
            "is_safe": True,
            "confidence": 0.95,
            "scanned_at": datetime.datetime(2024, 1, 1, 12, 0, 0),
            "explanation": '["safe domain"]',
        }
    ]
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = get_all_scans()
    assert len(result) == 1
    assert result[0]["url"] == "http://example.com"
    assert result[0]["explanation"] == "safe domain"

def test_get_all_scans_null_explanation():
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = [
        {
            "id": 2,
            "url": "http://test.com",
            "is_safe": False,
            "confidence": 0.20,
            "scanned_at": datetime.datetime(2024, 1, 2),
            "explanation": None,
        }
    ]
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = get_all_scans()
    assert result[0]["explanation"] == ""

def test_get_all_scans_empty():
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = []
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = get_all_scans()
    assert result == []

def test_get_all_scans_limit_capped():
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = []
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        get_all_scans(limit=9999)
    passed_limit = mock_cur.execute.call_args[0][1][0]
    assert passed_limit == 500

def test_get_all_scans_exception_returns_none():
    with patch("database.get_cursor", side_effect=Exception("db error")):
        result = get_all_scans()
    assert result is None

def test_delete_scan_success():
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = {"id": 1}
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = delete_scan(1)
    assert result is True

def test_delete_scan_not_found():
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = None
    with patch("database.get_cursor", _cursor_ctx(mock_cur)):
        result = delete_scan(999)
    assert result is False

def test_delete_scan_exception_returns_false():
    with patch("database.get_cursor", side_effect=Exception("db error")):
        result = delete_scan(1)
    assert result is False


