#!/usr/bin/python3
'''Creates Flask ap to register the blueprint app_views Flask instance app.'''

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    ''' function that removes the current SQLAl Session obj after each req'''
    storage.close()


# Error handlers for expected app behavior:
@app.errorhandler(404)
def not_found(error):
    ''' function that Returns errmsg `Not Found '''
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
