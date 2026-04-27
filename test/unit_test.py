# Unit tests for backend helper functions + API routes, runs without a live server or DB, mocked external dependencies
import sys
import os
import json
import pytest
from unittest.mock import patch

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
    assert res.status_code == 400
