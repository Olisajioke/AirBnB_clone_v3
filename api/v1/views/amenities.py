#!/usr/bin/python3
''' Module that Creates a view for Amenity objects.'''

from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def fetch_all_amenities():
    '''Function that retrieves the list of all Amenity objects'''
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_amenity(amenity_id):
    '''Function that retrieves an Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def remove_amenity(amenity_id):
    '''Function that deletes an Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    '''Function that creates an Amenity object'''
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_existing_amenity(amenity_id):
    '''Function that updates an Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def handle_not_found(error):
    """Function that handles error 404"""
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def handle_bad_request(error):
    """Function that handles bad request error"""
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
