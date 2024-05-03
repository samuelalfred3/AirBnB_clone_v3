#!/usr/bin/python3
"""
Module for handling index view.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of each object type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)

