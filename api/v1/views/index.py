#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route /status on the object app_views
that returns a JSON: "status": "OK"
"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """returns a JSON: "status": "OK" """
    return {"status": "OK"}


if __name__ == "__main__":
    app_views.run(host="0.0.0.0", port="5000")
