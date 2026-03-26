from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import re
from urllib.parse import urlparse, urlunparse, quote
import joblib
from sklearn.linear_model import LogisticRegression
from pathlib import Path as path
import datetime
import sys
from urllib.request import urlopen, URLError

from pipeline import model_pipeline


app = Flask(__name__)
model: str
# TODO:
# ADD WHITELIST
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


def check_valid_url(url):
    """
    Check if URL is valid using urllib.

    Args:
        url (str): URL link to be checked.

    Returns:
        bool: Returns True if the URL is valid.
    """
    if not url or not isinstance(url, str):
        return False

    try:
        urlopen(url)
        return True
    except URLError as e:
        print(e)
        return False
    except Exception as e:
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

    # check whether request is JSON
    if not request.is_json:
        msg = f"Invalid request from {request.remote_addr}: Not a JSON request"
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "send JSON request"}), 400

    # check whether request body is a JSON object 
    request_data = request.get_json()
    if not isinstance(request_data, dict):
        msg = f"{request.remote_addr}: Body is not JSON object"
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "invalid request body"}), 400

    # check if url field missing or not a string 
    url = request_data.get("url")
    if url is None or not isinstance(url, str):
        msg = f"{request.remote_addr}: Missing or invalid url field"
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "missing/invalid URL field"}), 400
    
    # check if url is valid format 
    if not check_valid_url(url):
        msg = f"Invalid URL from {request.remote_addr}: {url}"
        app.logger.warning(msg)
        write_log(msg, "ERROR")
        return jsonify({"error": "Invalid URL format"}), 400

    app.logger.info(type(request_data))

    sanitised_url = sanitise_url(url)
    url_obj = preprocess_data(sanitised_url)
    df = url_obj.get_data()
    # Model returns a np.array
    isSafe = model.predict(df)[0]
    confidence = model.predict_proba(df)[0] * 100.0
    # {notSafe = 0, safe = 1}

    print(isSafe)
    return (
        jsonify(
            {
                "isSafe": bool(isSafe),
                "confidence": float(confidence[1] if isSafe == 1 else confidence[0]),
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
    model: str = "./models/logit_model.pkl"
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5001)
