import json
from functools import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import re
from urllib.parse import urlparse, urlunparse, quote
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


# initial url validity check
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
    except URLError:
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


@app.route("/scan", methods=["POST"])
def check_url():
    """
    Route to check a URL from a given frontend.

    Args:
        url (str): URL link to be checked (from request body).

    Returns:
        JSON: Return the result if successful, otherwise returns a 400 error.
    """
    if not isinstance(request.json, dict):
        return jsonify({"error": "invalid request body"}), 400

    request_data = request.json
    url = request_data.get("url")
    if url is None:
        return jsonify({"error": "invalid request body"}), 400

    if not check_valid_url(url):
        app.logger.warning(f"Bad URL from {request.remote_addr}: {url[:100]}...")
        return jsonify({"error": "invalid url format"}), 400

    app.logger.info(type(request_data))

    sanitised_url = sanitise_url(url)

    is_safe, confidence = models_pipeline(sanitised_url, model)

    print(is_safe)
    return jsonify(
        {"is_safe": bool(is_safe), 
         "confidence": float(confidence[1] if is_safe == 1 else confidence[0])
         }), 200


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

    if not isinstance(info, str) or info is None:
        return jsonify({"error": "empty information field"}), 400

    with open("error-log.txt", "a", encoding="latin-1") as f:
        f.write(info)

    return jsonify(True), 200


if __name__ == "__main__":
    model: str = "backend/models/logit_model.pkl"
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5001)
