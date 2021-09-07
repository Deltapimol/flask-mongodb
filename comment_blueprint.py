from datetime import date, datetime

from flask import Blueprint, jsonify, request

from flask_pymongo import PyMongo
import pymongo

from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from bson.json_util import dumps
from bson.objectid import ObjectId
from bson.errors import InvalidId

from config import mongo as mongodb_client


comment_blueprint = Blueprint("comment", import_name=__name__)

@comment_blueprint.route('', methods=['POST'])
def add_comment():
    """
    Add a new comment
    """
    _json = request.json
    _comment = _json['comment']
    _email = _json['email']
    _blog_id = _json['blog_id']
    
    if not _comment or len(_comment) == 0:  
        return jsonify("Comment cannot be empty!"), 400
    elif not _email:  
        return invalid_request("user email")
    elif not _blog_id:
        return invalid_request("blog id")

    if len(_comment) > 150:
        return jsonify("Comment cannot exceed 150 characters!"), 400
    try:
        try:
            user = mongodb_client.db.users.find_one({"email": _email}, {"password": False})
            if user is None:
                return jsonify(f"User with this email does not exist"), 404
        except InvalidId:
            return invalid_id("User")
        try:
            blog = mongodb_client.db.blogs.find_one({"_id": ObjectId(_blog_id)})
            if blog is None:
                return jsonify(f"Blog does not exist"), 404
        except InvalidId:
            return InvalidId("Blog")
        
        _create_time = datetime.now()
        _update_time = None
        
        comment = mongodb_client.db.comments.insert_one({"commentator": user['name'], "email": user["email"], "comment": _comment, "create_time": _create_time, "update_time": _update_time})
        print(comment, type(comment))
        comment_dict = {"comment_id": comment.inserted_id, "commentator": user['name'], "email": user["email"], "comment": _comment, "create_time": _create_time, "update_time": _update_time }
        mongodb_client.db.blogs.update({"_id": ObjectId(_blog_id)}, { "$push": {"comments": comment_dict}})
        return jsonify("Comment added successfully"), 200
    except Exception as e:
        return jsonify(e), 500
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@comment_blueprint.app_errorhandler(400)
def invalid_request(entity):
    message = f"Invalid request ({entity} required)!"
    return jsonify(message), 400

@comment_blueprint.app_errorhandler(400)
def invalid_id(entity):
    message = f"Invalid {entity} Id"
    return jsonify(message), 400

@comment_blueprint.app_errorhandler(404)
def not_found():
    message = "Not Found " + request.url
    return jsonify(message), 404

@comment_blueprint.app_errorhandler(500)
def database_connection_error():
    message = "Unable to connect to the MongoDB server"
    return jsonify(message), 500
    