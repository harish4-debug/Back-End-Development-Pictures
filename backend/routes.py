from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        return jsonify(data), 200
    except NameError:
        return {"message": "Data not found"}, 404

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        new_picture = request.get_json()
        if not new_picture:
            return {"message": "Invalid input, no data provided"}, 400

        id = new_picture['id']
        old_picture = None
        for picture in data:
            if picture["id"] == id:
                old_picture = picture

        if not old_picture:
            # picture does not exit.
            data[len(data)-1] = new_picture
            return jsonify(data), 201
        else:
            return jsonify({"message":f"picture with id {new_picture['id']} already present"}), 302

    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "details": str(e)
        }), 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
