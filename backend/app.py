import json
from functools import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import re 
from urllib.parse import urlparse, urlunparse, quote

app = Flask(__name__)
# TODO:
# DONT FUCKING ALLOW ALL ROUTES TO BE CROSS ORIGIN RESOURCE SHARED
# ADD WHITELIST
# CORS for frontend only
CORS(app, resources={r"/scan": {"origins: [http://localhost:5173/]"}})

# initial url validity check
def check_valid_url(url):
    if not url or not isinstance(url, str):
        return False
    # ensure url starts with http(s)://
    if not re.match(r'^https?://.+', url, re.IGNORECASE):
        return False
    
    return True 

# strip leading/trailing spaces, encode path to prevent xss/sqli
def sanitise_url(url):
    url = url.strip()
    parsed_url = urlparse(url)

    # encode path and query to prevent sqli + xss
    path = quote(parsed_url.path, safe="/")
    query = quote(parsed_url.query, safe="=&")

    sanitised_url = urlunparse((parsed_url.scheme, parsed_url.netloc, path, parsed_url.params, query, parsed_url.fragment))

    return sanitised_url

@app.route("/scan", methods=["POST"])
def check_url():
    """
    Route to check a URL
    param url: The url link to be checked (from request body)
    return: The results if successful
    """
    if not isinstance(request.json, dict):
        return jsonify({"error": "invalid request body"}), 400

    request_data = request.json
    url = request_data.get("url")

    if not check_valid_url(url):
        app.logger.warning(f"Bad URL from {request.remote_addr}: {url[:100]}...")
        return jsonify({"error": "invalid url format"}), 400
    
    sanitised_url = sanitise_url(url)

    app.logger.info(type(request_data))
    if url == "realwebsite.com":
        return jsonify(True), 200
    else:
        return jsonify(False), 200


if __name__ == "__main__":
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5001)
