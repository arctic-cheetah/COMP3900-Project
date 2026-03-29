import pandas
import requests
import os
import backend.preprocessor as p


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
