#!/usr/bin/python3
""" Module that creates a new view for State objects"""
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


# Route for retrieving all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Function that retrieves the list of all State objects."""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


# Route for retrieving a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Function that retrieves a State object."""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


# Route for deleting a specific State object by ID
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Function that  deletes a State object."""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# Route for creating a new State object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Function that  Creates a State object."""
    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


# Function thatworks to route for updating an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Function that Updates a States"""
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        state.save()
        # This returns the updated State object in JSON with 200 status msg
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


# The following are the Error Handlers with error  messages:
@app_views.errorhandler(404)
def not_found(error):
    """ Function that raises a 404 error with message."""
    # this returns a JSON response for 404 error and displays msg
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """ function that returns a Bad Request msg for illegal requests to API"""
    # this returns a JSON response for 400 error and displays msg
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
