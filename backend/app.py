import json
from functools import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

app = Flask(__name__)
# TODO:
# DONT FUCKING ALLOW ALL ROUTES TO BE CROSS ORIGIN RESOURCE SHARED
# ADD WHITELIST
allowedOrigins = ["127.0.0.1:80", "127.0.0.1:6969"]
corsConfig = {"origins": allowedOrigins}
CORS(app, resources={r"/*": corsConfig})


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
        return jsonify({"error": "invalid request body"}), 400

    request_data = request.json
    url = request_data.get("url")

    # TODO: SOmeone needs to do more error checking for url here!!
    # Like https or http
    if not isinstance(url, str) or url is None:
        return jsonify({"error": "url is not valid"}), 400

    app.logger.info(type(request_data))
    if url == "realwebsite.com":
        return jsonify(True), 200
    else:
        return jsonify(False), 200


@app.route("/error", methods=["POST"])
def log_error():
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
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5001)
