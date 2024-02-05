#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions:

In the file api/v1/views/places.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all Place objects of a
City: GET /api/v1/cities/<city_id>/places

If the city_id is not linked to any City object, raise a 404 error
Retrieves a Place object. : GET /api/v1/places/<place_id>

If the place_id is not linked to any Place object, raise a 404 error
Deletes a Place object: DELETE /api/v1/places/<place_id>

If the place_id is not linked to any Place object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a Place: POST /api/v1/cities/<city_id>/places

You must use request.get_json from Flask to transform
the HTTP request to a dictionary
If the city_id is not linked to any City object, raise a 404 error
If the HTTP request body is not valid JSON, raise
a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key user_id,
raise a 400 error with the message Missing user_id
If the user_id is not linked to any User object, raise a 404 error
If the dictionary doesn’t contain the key name,
raise a 400 error with the message Missing name
Returns the new Place with the status code 201
Updates a Place object: PUT /api/v1/places/<place_id>

If the place_id is not linked to any Place object, raise a 404 error
You must use request.get_json from Flask to
transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON,
raise a 400 error with the message Not a JSON
Update the Place object with all key-value
pairs of the dictionary
Ignore keys: id, user_id, city_id, created_at and updated_at
Returns the Place object with the status code 200
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def list_places(city_id):
    '''Retrieves the list of all Place objects'''
    all_places = storage.all("Place").values()
    list_places = [obj.to_dict() for obj in all_places
                   if obj.city_id == city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Retrieves a Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places
                 if obj.id == place_id]
    if place_obj:
        return jsonify(place_obj[0])
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a Place object'''
    place_obj = storage.get("Place", place_id)
    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a Place'''
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if not storage.get("User", request.get_json()['user_id']):
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    new_place = Place(**request.get_json())
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    '''Updates a Place object'''
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict())
