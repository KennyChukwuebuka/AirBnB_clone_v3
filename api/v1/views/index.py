#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route /status on the object app_views
that returns a JSON: "status": "OK"

Create an endpoint that retrieves the number of each objects by type:

In api/v1/views/index.py
Route: /api/v1/stats
You must use the newly added count() method from storage
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    ''' routes to stats page '''
    from models import storage
    from models.user import User
    return jsonify({
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    })
