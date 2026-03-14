import json
from functools import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import re
from urllib.parse import urlparse, urlunparse, quote
import joblib
from sklearn.linear_model import LogisticRegression
from preprocessor import preprocess_data
from pathlib import Path as path
import datetime
import sys

app = Flask(__name__)
model: LogisticRegression
# TODO:
# DONT FUCKING ALLOW ALL ROUTES TO BE CROSS ORIGIN RESOURCE SHARED
# ADD WHITELIST
allowedOrigins = [
    "http://127.0.0.1:80",
    "http://127.0.0.1:6969",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:6969",
]
corsConfig = {"origins": allowedOrigins}
CORS(app, resources={r"/*": corsConfig})

# log directory details
LOG_DIR = path("logs")
LOG_DIR.mkdir(exist_ok=True)
ERROR_LOG = LOG_DIR / "api_errors.txt"
CRITICAL_LOG = LOG_DIR / "critical_failures.txt"

# logging config to file + console
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "app.txt"),
        logging.StreamHandler()
    ]
)

# logs a JSON entry to the appropriate log file based on log type
# log type is either ERROR or CRITICAL
def write_log(msg, log_type):

    timestamp = datetime.datetime.utcnow().isoformat()
    entry = {
        "timestamp": timestamp, 
        "log_type": log_type, 
        "message": msg
    }

    target_file = ERROR_LOG if log_type == "ERROR" else CRITICAL_LOG

    try:
        with open(target_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"LOGGING FAILED: {str(e)}", file=sys.stderr)

# initial url validity check
def check_valid_url(url):
    if not url or not isinstance(url, str):
        return False
    # ensure url starts with http(s)://
    if not re.match(r"^https?://.+", url, re.IGNORECASE):
        return False

    return True


# strip leading/trailing spaces, encode path to prevent xss/sqli
def sanitise_url(url):
    url = url.strip()
    parsed_url = urlparse(url)

    # encode path and query to prevent sqli + xss
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


@app.route("/scan", methods=["POST"])
def check_url():
    """
    Route to check a URL from a given frontend
    Args:
        param url: The url link to be checked (from request body)
        param1: request object with json inside
    Returns:
        return: The results if successful otherwise return 400 error
    """
    if not isinstance(request.json, dict):
        write_log("invalid request body", ERROR_LOG)
        return jsonify({"error": "invalid request body"}), 400

    request_data = request.json
    url = request_data.get("url")
    if url is None:
        return jsonify({"error": "invalid request body"}), 400

    if not check_valid_url(url):
        app.logger.warning(f"Bad URL from {request.remote_addr}: {url[:100]}...")
        write_log(f"Bad URL from {request.remote_addr}: {url[:100]}...", ERROR_LOG)
        return jsonify({"error": "invalid url format"}), 400

    app.logger.info(type(request_data))

    sanitised_url = sanitise_url(url)
    url_obj = preprocess_data(sanitised_url)
    df = url_obj.get_data()
    # Model returns a np.array
    isSafe = model.predict(df)[0]
    if isSafe:
        return jsonify(True), 200
    else:
        return jsonify(False), 200


@app.route("/error", methods=["POST"])
def log_error():
    """
    Route to log errors from the ai model
    Args:
        param info: The information to be logged (from request body)
        param1: request object with json inside
    Returns:
        return: The results if successful otherwise return 400 error
    """
    # TODO: please throw exceptions from AI model to this route for logging
    if not isinstance(request.json, dict):
        return jsonify({"error": "invalid request body"}), 400

    request_data = request.json
    info = request_data.get("info")
    level = request_data.get("level", "ERROR")

    if not isinstance(info, str) or info is None:
        return jsonify({"error": "empty information field"}), 400
    
    # add IP addr which triggered error + log level to context
    context = f"[{request.remote_addr}] {info}"

    write_log(context, level)

    return jsonify(True), 200


if __name__ == "__main__":
    model: LogisticRegression = joblib.load("backend/models/logit_model.pkl")
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5001)
