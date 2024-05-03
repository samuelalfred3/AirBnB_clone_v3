#!/usr/bin/python3
"""Place API views module."""
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object by id."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object by id."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place object."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")
    user_id = data["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    place = Place(city_id=city_id, **data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object by id."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Search for Place objects based on JSON data."""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")

    states = json_data.get('states', [])
    cities = json_data.get('cities', [])
    amenities = json_data.get('amenities', [])

    places = []
    if not states and not cities:
        places = storage.all('Place').values()
    else:
        if states:
            for state_id in states:
                state = storage.get('State', state_id)
                if state:
                    cities.extend([city.id for city in state.cities])
        for city_id in cities:
            city = storage.get('City', city_id)
            if city:
                places.extend(city.places)

    if amenities:
        places = [place for place in places if all(
            amenity_id in [amenity.id for amenity in place.amenities]
            for amenity_id in amenities)]

    places_json = [place.to_dict() for place in places]
    return jsonify(places_json), 200

