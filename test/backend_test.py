import pandas
import requests
import os
import backend.ml.preprocessor as p


sites_test = "realwebsite.com"
# USE THIS URL IF RUNNING EVERTHING LOCALLY
URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5001")
headers = {"Content-Type": "application/json"}
payload = {"url": sites_test}
SCAN = "/scan"
ERROR = "/error"
s = requests.session()


# These are the test cases for backend
def test_url_scan_route_is_post():
    req = requests.Request("POST", URL + SCAN, headers=headers, data=payload)
    prep = s.prepare_request(req)
    res = s.send(prep)
    assert res.status_code != 404
    print(res.text)


def test_invalid_body_scan():
    req = requests.Request(
        "POST", URL + SCAN, headers=headers, data={"urls": sites_test}
    )
    prep = s.prepare_request(req)
    res = s.send(prep)
    assert res.status_code == 400
    print(res.text)


def test_invalid_url_to_scan():
    req = requests.Request("POST", URL + SCAN, headers=headers, data={"urls": 123})
    prep = s.prepare_request(req)
    res = s.send(prep)
    assert res.status_code == 400
    print(res.text)


def test_backend_has_error_log():
    req = requests.Request("POST", URL + ERROR, headers=headers, data=payload)
    prep = s.prepare_request(req)
    res = s.send(prep)
    assert res.status_code != 404
    print(res.text)


def test_backend_reject_malformed():
    req = requests.Request("POST", URL + ERROR, headers=headers, data=payload)
    prep = s.prepare_request(req)
    res = s.send(prep)
    assert res.status_code == 400
    print(res.text)

def test_scan_is_persistent():
    res = s.post(URL + SCAN, json={"url": "https://www.microsoft.com/"})
    assert res.status_code == 200

    scans = s.get(URL + "/scans")
    assert scans.status_code == 200
    urls = [scan["url"] for scan in scans.json()["scans"]]
    assert any("microsoft.com" in u for u in urls)


def test_list_scans_returns_expected_fields():
    res = s.get(URL + "/scans")
    assert res.status_code == 200
    data = res.json()
    assert "scans" in data
    if data["scans"]:
        scan = data["scans"][0]
        for field in ["id", "url", "is_safe", "confidence", "scanned_at"]:
            assert field in scan, f"missing field: {field}"


def test_list_scans_pagination():
    res = s.get(URL + "/scans", params={"limit": 2, "offset": 0})
    assert res.status_code == 200
    assert len(res.json()["scans"]) <= 2


def test_list_scans_invalid_parameters():
    res = s.get(URL + "/scans", params={"limit": "abc"})
    assert res.status_code == 400


def test_delete_scan():
    s.post(URL + SCAN, json={"url": "https://www.microsoft.com/"})

    scans = s.get(URL + "/scans")
    scan_id = scans.json()["scans"][0]["id"]

    res = s.delete(f"{URL}/scans/{scan_id}")
    assert res.status_code == 200
    assert res.json()["deleted"] == scan_id

    after = s.get(URL + "/scans")
    remaining_ids = [sc["id"] for sc in after.json()["scans"]]
    assert scan_id not in remaining_ids


def test_delete_nonexistent_scan():
    res = s.delete(f"{URL}/scans/999999")
    assert res.status_code == 404


def test_export_returns_csv():
    res = s.get(URL + "/scans/export")
    assert res.status_code == 200
    assert "text/csv" in res.headers.get("Content-Type", "")

    lines = res.text.strip().split("\n")
    assert lines[0] == "id,url,is_safe,confidence,timestamp"
    print(f"exported {len(lines) - 1} rows")
