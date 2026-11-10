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
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if id in [d["id"] for d in data]:
        return jsonify([d for d in data if d["id"]==id][0]), 200
    return {"message": "Picture nto found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    d = request.get_json()
    # breakpoint()
    if not d["id"] in [di["id"] for di in data]:
        data.append(d)
        return jsonify(d), 201
    else:
        return {"Message": f"picture with id {d['id']} already present"}, 302

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_d = request.get_json()
    if id in [d["id"] for d in data]:
        i = [i for i,d in enumerate(data) if d["id"]==id][0]
        data[i] = new_d
        return {"message": "good"}, 200
    return {"message": "Picture nto found"}, 400

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if id in [d["id"] for d in data]:
        i = [i for i,d in enumerate(data) if d["id"]==id][0]
        data.pop(i)
        return {"message": "good"}, 204
    return {"message": "Picture nto found"}, 404
