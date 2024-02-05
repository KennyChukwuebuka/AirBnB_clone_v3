#!/usr/bin/python3
"""
Create a new view for Amenity objects
that handles all default RESTFul API actions:

In the file api/v1/views/amenities.py
You must use to_dict() to serialize an object into valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all Amenity objects: GET /api/v1/amenities

Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a 404 error
Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a Amenity: POST /api/v1/amenities

You must use request.get_json from
Flask to transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON,
raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key
name, raise a 400 error with the message Missing name
Returns the new Amenity with the status code 201
Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity
object, raise a 404 error
You must use request.get_json from Flask
to transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON,
raise a 400 error with the message Not a JSON
Update the Amenity object with all key-value
pairs of the dictionary
Ignore keys: id, created_at and updated_at
Returns the Amenity object with the status code 200
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities', methods=['GET'])
def list_amenities():
    '''Retrieves a list of all Amenity objects'''
    list_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    '''Retrieves a Amenity object'''
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes a Amenity object'''
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    amenity_obj.remove(amenity_obj[0])
    for obj in all_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    '''Creates a Amenity'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    '''Updates a Amenity object'''
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj[0], key, value)
    storage.save()
    return jsonify(amenity_obj[0])
