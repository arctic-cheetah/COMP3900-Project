import json
from functools import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

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

    if not isinstance(url, str) or url is None:
        return jsonify({"error": "url is not valid"}), 400
    
    app.logger.info(type(request_data))
    return jsonify(), 200


if __name__ == "__main__":
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5000)
