#!/usr/bin/python3
''' Module that creates a new view for City objects'''

from flask import abort, jsonify, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def fetch_cities_by_state(state_id):
    ''' Function that retrieves list of all City objs of a jsonify State'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def fetch_city(city_id):
    ''' Function that retrieves a City object and returns the jsonify obj'''
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def remove_city(city_id):
    ''' Function that deletes a City object with jsonify'''
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_new_city(state_id):
    ''' Function that creates a City object with json'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_existing_city(city_id):
    ''' Function that updates a City object with json'''
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def handle_not_found(error):
    ''' Function that returns 404: Not Found with message'''
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def handle_bad_request(error):
    '''Function that returns a bad Request msg for illegal requests to API'''
    # Return a JSON response for 400 error
    return jsonify({'error': 'Bad Request'}), 400