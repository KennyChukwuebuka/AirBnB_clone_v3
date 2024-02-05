#!/usr/bin/python3
"""
Create a new view for User object that handles all default RESTFul API actions:

In the file api/v1/views/users.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all User objects: GET /api/v1/users

Retrieves a User object: GET /api/v1/users/<user_id>

If the user_id is not linked to any User object, raise a 404 error
Deletes a User object:: DELETE /api/v1/users/<user_id>

If the user_id is not linked to any User object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a User: POST /api/v1/users

You must use request.get_json from Flask
to transform the HTTP body request to a dictionary
If the HTTP body request is not valid JSON,
raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key email,
raise a 400 error with the message Missing email
If the dictionary doesn’t contain the key password,
raise a 400 error with the message Missing password
Returns the new User with the status code 201
Updates a User object: PUT /api/v1/users/<user_id>

If the user_id is not linked to any User object, raise a 404 error
You must use request.get_json from Flask to
transform the HTTP body request to a dictionary
If the HTTP body request is not valid JSON,
raise a 400 error with the message Not a JSON
Update the User object with all key-value
pairs of the dictionary
Ignore keys: id, email, created_at and updated_at
Returns the User object with the status code 200
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users', methods=['GET'])
def list_users():
    '''Retrieves a list of all User objects'''
    list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''Retrieves a User object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    return jsonify(user_obj[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes a User object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    user_obj.remove(user_obj[0])
    for obj in all_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    '''Creates a User'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    users = []
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    '''Updates a User object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj[0], key, value)
    storage.save()
    return jsonify(user_obj[0])
