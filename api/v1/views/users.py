#!/usr/bin/python3
"""User API views module."""
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects."""
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object by id."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object by id."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User object."""
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object by id."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

