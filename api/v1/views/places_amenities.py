#!/usr/bin/python3
"""Handles RESTful API actions for Place-Amenity interactions"""

from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities_updated.yml',
           methods=['GET'])
def retrieve_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects associated with a Place
    """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amen.to_dict() for amen in place_obj.amenities]
    else:
        amenities = [storage.get(Amenity, amen_id).to_dict()
                     for amen_id in place_obj.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities_updated.yml',
           methods=['DELETE'])
def remove_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object associated with a Place
    """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        place_obj.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST']
                 ,strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities_updated.yml',
           methods=['POST'])
def add_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place
    """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity_obj in place_obj.amenities:
            return make_response(jsonify(amenity_obj.to_dict()), 200)
        else:
            place_obj.amenities.append(amenity_obj)
    else:
        if amenity_id in place_obj.amenity_ids:
            return make_response(jsonify(amenity_obj.to_dict()), 200)
        else:
            place_obj.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)
