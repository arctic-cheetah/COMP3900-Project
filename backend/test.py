import requests

BASE = "http://localhost:5001"


def test_scan(url, expected_status=200):
    r = requests.post(
        f"{BASE}/scan", json={"url": url}, headers={"Content-Type": "application/json"}
    )

    print(f"[{r.status_code}] {url[:60]} -> {r.json()}")
    return r.status_code == expected_status
