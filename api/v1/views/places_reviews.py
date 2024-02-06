#!/usr/bin/python3
"""
Create a new view for Review object that
handles all default RESTFul API actions:

In the file api/v1/views/places_reviews.py
You must use to_dict() to retrieve an object into valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all Review objects
of a Place: GET /api/v1/places/<place_id>/reviews

If the place_id is not linked to any Place object, raise a 404 error
Retrieves a Review object. : GET /api/v1/reviews/<review_id>

If the review_id is not linked to any Review object, raise a 404 error
Deletes a Review object: DELETE /api/v1/reviews/<review_id>

If the review_id is not linked to any Review object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a Review: POST /api/v1/places/<place_id>/reviews

You must use request.get_json from Flask
to transform the HTTP request to a dictionary
If the place_id is not linked to any Place
object, raise a 404 error
If the HTTP body request is not valid JSON,
raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key
user_id, raise a 400 error with the message Missing user_id
If the user_id is not linked to any User
object, raise a 404 error
If the dictionary doesn’t contain the key
text, raise a 400 error with the message Missing text
Returns the new Review with the status code 201
Updates a Review object: PUT /api/v1/reviews/<review_id>

If the review_id is not linked to any
Review object, raise a 404 error
You must use request.get_json from Flask
to transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON,
raise a 400 error with the message Not a JSON
Update the Review object with all key-value
pairs of the dictionary
Ignore keys: id, user_id, place_id, created_at and updated_at
Returns the Review object with the status code 200
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def list_reviews(place_id):
    '''Retrieves the list of all Review objects'''
    all_reviews = storage.all("Review").values()
    list_reviews = [obj.to_dict() for obj in all_reviews
                    if obj.place_id == place_id]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    '''Retrieves a Review object'''
    all_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in all_reviews
                  if obj.id == review_id]
    if not review_obj:
        abort(404)
    return jsonify(review_obj[0])


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''Deletes a Review object'''
    all_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in all_reviews
                  if obj.id == review_id]
    if not review_obj:
        abort(404)
    review_obj.remove(review_obj[0])
    for obj in all_reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    '''Creates a Review'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    user_obj = storage.get("User", request.get_json()['user_id'])
    if not user_obj:
        abort(404)
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    review_obj = Review(**request.get_json())
    review_obj.place_id = place_id
    review_obj.id = str(uuid.uuid4())
    review_obj.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    '''Updates a Review object'''
    all_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in all_reviews
                  if obj.id == review_id]
    if not review_obj:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review_obj[0], key, value)
    review_obj[0].save()
    return jsonify(review_obj[0].to_dict()), 200
