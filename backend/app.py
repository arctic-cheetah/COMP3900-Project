import json
from functools import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import re
from urllib.parse import urlparse, urlunparse, quote
from sklearn.linear_model import LogisticRegression
from pathlib import Path as path
import datetime
import sys
from urllib.request import urlopen, URLError
from urllib.parse import urlparse
import tldextract
import csv
import io
from ml.pipeline import model_pipeline
from database import init_db, save_scan, get_all_scans, delete_scan


app = Flask(__name__)
CORS(app)

allowed_origins = [
    "http://127.0.0.1:80",
    "http://127.0.0.1:6969",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:6969",
]
cors_config = {"origins": allowed_origins}
CORS(app, resources={r"/*": cors_config})

# log directory details
LOG_DIR = path("logs")
LOG_DIR.mkdir(exist_ok=True)
ERROR_LOG = LOG_DIR / "api_errors.txt"
CRITICAL_LOG = LOG_DIR / "critical_failures.txt"

# logging config to file + console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "app.txt"), logging.StreamHandler()],
)


# logs a JSON entry to the appropriate log file based on log type
# log type is either ERROR or CRITICAL
def write_log(msg, log_type):
    timestamp = datetime.datetime.utcnow().isoformat()
    entry = {"timestamp": timestamp, "log_type": log_type, "message": msg}

    target_file = ERROR_LOG if log_type == "ERROR" else CRITICAL_LOG

    try:
        with open(target_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"LOGGING FAILED: {str(e)}", file=sys.stderr)


def check_valid_url(url):
    """
    Check if URL has valid syntax using tldextract.

    Args:
        url (str): URL link to be checked.

    Returns:
        bool: Returns True if the URL has valid syntax.
    """
    if not url or not isinstance(url, str):
        return False

    # BUG We should not test validity of url with reachability
    try:
        ext = tldextract.extract(url)

        if ext.domain and ext.suffix:
            return True
    except Exception as e:
        print(e)

    return False


def sanitise_url(url):
    """
    Sanitise URL by stripping leading/trailing spaces and encodes path to prevent XSS/SQLI.

    Args:
        url (str): URL link to be sanitised.

    Returns:
        str: Returns the sanitised URL.
    """
    url = url.strip()
    parsed_url = urlparse(url)

    # encode path and query to prevent XSS/SQLI
    path = quote(parsed_url.path, safe="/")
    query = quote(parsed_url.query, safe="=&")

    sanitised_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            path,
            parsed_url.params,
            query,
            parsed_url.fragment,
        )
    )

    return sanitised_url


@app.route("/", methods=["GET"])
def health_check():
    return "Working!", 200


@app.route("/scan", methods=["POST"])
def check_url():
    """
    Route to check a URL from a given frontend.

    Args:
        url (str): URL link to be checked (from request body).

    Returns:
        JSON: Return the result if successful, otherwise returns a 400 error.
    """
    if not request.is_json:
        msg = f"{request.remote_addr}: Not a JSON request"
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "Send JSON request"}), 400

    request_data = request.get_json()
    if not isinstance(request_data, dict):
        msg = f"{request.remote_addr}: Body is not JSON object"
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "Invalid request body"}), 400

    url = request_data.get("url")
    if url is None or not isinstance(url, str):
        msg = f"{request.remote_addr}: Missing or invalid url field"
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "Missing/Invalid URL field"}), 400

    url_scheme = urlparse(url).scheme
    if url_scheme and (url_scheme != "http" and url_scheme != "https"):
        msg = f'{request.remote_addr}: Invalid URL scheme in "{url}"'
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "Invalid URL scheme"}), 400
    if not url_scheme:
        url = "http://" + url

    if not check_valid_url(url):
        msg = f'{request.remote_addr}: Invalid URL "{url}"'
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "Invalid URL format"}), 400

    sanitised_url = sanitise_url(url)
    try:
        res = model_pipeline(sanitised_url)
        if res is None:
            raise Exception
        else:
            is_safe, confidence_score, explanations = res
        # persistence while maintaining anynomity
        # TODO: CHECK IF THIS VULN having dangling saved
        saved = save_scan(
            url=sanitised_url,
            is_safe=bool(is_safe),
            confidence=confidence_score,
            explanation=explanations,
        )

        return (
            jsonify(
                {
                    "is_safe": bool(is_safe),
                    "confidence": confidence_score,
                    "explanations": explanations,
                }
            ),
            200,
        )
    except Exception as e:
        app.logger.error("Scan failed: %s", e)
        return jsonify({"error": "URL could not be scanned"}), 400


@app.route("/list_scans", methods=["POST"])
# Return paginated scan history from scans table with most recent first
@app.route("/scans", methods=["GET"])
def list_scans():
    try:
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit and offset must be integers"}), 400

    if limit < 1 or offset < 0:
        return jsonify({"error": "limit must be >= 1 and offset must be >= 0"}), 400

    scans = get_all_scans(limit=limit, offset=offset)

    if scans is None:
        return jsonify({"error": "could not retrieve scan history"}), 500

    return (
        jsonify(
            {
                "scans": scans,
                "limit": limit,
                "offset": offset,
            }
        ),
        200,
    )


@app.route("/error", methods=["POST"])
def log_error():
    """
    Route to log errors from the ML model.

    Args:
        info: The information to be logged (from request body)

    Returns:
        JSON: Return True if successful, otherwise returns a 400 error.
    """
    # TODO: please throw exceptions from AI model to this route for logging
    if not isinstance(request.json, dict):
        return jsonify({"error": "Invalid request body"}), 400

    request_data = request.json
    info = request_data.get("info")
    level = request_data.get("level", "ERROR")

    if not isinstance(info, str) or info is None:
        return jsonify({"error": "Empty information field"}), 400

    context = f"[{request.remote_addr}] {info}"

    write_log(context, level)

    return jsonify(True), 200


# Delete scan by ID, return 404 if not found, else return deleted ID
@app.route("/scans/<int:scan_id>", methods=["DELETE"])
def remove_scan(scan_id):
    success = delete_scan(scan_id)
    if not success:
        return jsonify({"error": "scan not found"}), 404
    return jsonify({"deleted": scan_id}), 200


# Export scan history as scan_history.csv, return 500 if scan history unable to be retrieved
@app.route("/scans/export", methods=["GET"])
def export_scans():
    scans = get_all_scans(limit=10000, offset=0)
    if scans is None:
        return jsonify({"error": "could not retrieve scan history"}), 500

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["id", "url", "is_safe", "confidence", "scanned_at", "explanation"],
    )
    writer.writeheader()
    writer.writerows(scans)
    headers = {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=scan_history.csv",
    }
    return output.getvalue(), 200, headers


if __name__ == "__main__":
    app.logger.setLevel(logging.INFO)
    init_db()
    app.run(host="0.0.0.0", port=5001)
