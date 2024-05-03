#!/usr/bin/python3
"""
Module for handling the Flask app and its routes.
"""
from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = '0.0.0.0'  # Environment variable HBNB_API_HOST or default '0.0.0.0'
    port = '5000'     # Environment variable HBNB_API_PORT or default '5000'
    app.run(host=host, port=port)

