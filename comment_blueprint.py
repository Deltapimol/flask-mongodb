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

# Fixes needed here
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
        mongodb_client.db.blogs.find_one_and_update({"_id": ObjectId(_blog_id)}, {'$push': {'comments': comment.inserted_id}})
        comment_dict = {"comment_id": comment.inserted_id, "commentator": user['name'], "email": user["email"], "comment": _comment, "create_time": _create_time, "update_time": _update_time }
        
        # mongodb_client.db.blogs.update({"_id": ObjectId(_blog_id)}, { "$push": {"comments": comment_dict}})
        return jsonify("Comment added successfully"), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()
    except Exception as e:
        return jsonify(e), 500

# Fixes needed here
@comment_blueprint.route('/<id>', methods=['PUT'])
def update_comment(id):
    """
    Update a comment
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
    
    pass
    # try:
    #     author = mongodb_client.db.users.find_one({'email': _email} , {'password': False})
    #     if author is None:
    #         return jsonify(f"User with this email does not exist"), 404
    #     try:
    #         blog = mongodb_client.db.blogs.find_one({'_id': ObjectId(id)})
    #     except InvalidId:
    #         return invalid_id("User")
        
    #     if blog is None:
    #         return jsonify("Blog does not exist"), 404
        
    #     _published = blog['published']
    #     _publish_date = blog['publish_date']
        
    #     if "publish" in _json and _json["publish"] != _published:
    #         _published = _json["publish"]
    #         if _published == True:
    #             _publish_date = datetime.now()
    #         elif _published == False:
    #            _publish_date = None
            
    #     mongodb_client.db.blogs.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'title': _title, 'text': _text, 'author': _author, 'email': _email, 'create_date': blog['create_date'], 'publish_date': _publish_date, 'published': _published, 'update_date': datetime.now()}})
        
    #     return jsonify("Blog updated successfully!"), 200
    # except (ServerSelectionTimeoutError, ConnectionFailure):
    #     return database_connection_error()

# Fixes needed here
@comment_blueprint.route('/<comment_id>', methods=['DELETE'])
def delete_comment():
    """
    Add a new comment
    """
    pass

@comment_blueprint.route('/reply', methods=['POST'])
def add_reply():
    """
    Add a reply to a comment
    """
    _json = request.json
    _email = _json['email']
    _reply = _json['reply']
    _comment_id = _json['comment_id']
    
    if _reply is None or len(_reply) == 0:
        return jsonify("Comment cannot be empty!"), 400
    elif not _email:  
        return invalid_request("user email")
    elif not _comment_id:
        return invalid_request("comment id")

    if len(_reply) > 100:
        return jsonify("Reply cannot exceed 150 characters!"), 400
    
    try:
        try:
            user = mongodb_client.db.users.find_one({"email": _email}, {"password": False})
            if user is None:
                return jsonify(f"User with this email does not exist"), 404
        except InvalidId:
            return invalid_id("User")
        
        _reply_dict = {'_id': ObjectId(), 'email': _email, 'respondent': user['name'], 'reply': _reply, 'create_time': datetime.now(), 'update_time': None}

        try:
            mongodb_client.db.comments.find_one_and_update({'_id': ObjectId(_comment_id)}, { '$push': {'replies': _reply_dict}})
        except InvalidId:
            return invalid_id("Comment")
        return jsonify("Reply added successfully"), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@comment_blueprint.route('/reply', methods=['PUT'])
def edit_reply():
    """
    Update a reply
    """
    _json = request.json
    _email = _json['email']
    _reply = _json['reply']
    _comment_id = _json['comment_id']
    _reply_id = _json['reply_id']
    
    if _reply is None or len(_reply) == 0:
        return jsonify("Comment cannot be empty!"), 400
    elif not _email:  
        return invalid_request("user email")
    elif not _comment_id:
        return invalid_request("comment id")

    if len(_reply) > 100:
        return jsonify("Reply cannot exceed 150 characters!"), 400
    try:
        try:
            user = mongodb_client.db.users.find_one({"email": _email}, {"password": False})
            if user is None:
                return jsonify(f"User with this email does not exist"), 404
        except InvalidId:
            return invalid_id("User")
        try:
            reply = mongodb_client.db.comments.find_one_and_update({'_id': ObjectId(_comment_id), 'replies._id': ObjectId(_reply_id)}, {'$set': {'replies.$.reply': _reply, 'replies.$.update_time': datetime.now()}})
        except InvalidId:
            return invalid_id()
        return jsonify("Reply edited successfully"), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@comment_blueprint.route('/<comment_id>/reply/<reply_id>', methods=['DELETE'])
def delete_reply(comment_id, reply_id):
    """
    Delete a reply
    """
    try:
        try:
            reply = mongodb_client.db.comments.find_one_and_update({'_id': ObjectId(comment_id)}, {'$pull': {'replies': {'_id': ObjectId(reply_id)}}})
            return jsonify("Reply deleted successfully")
        except InvalidId:
            return invalid_id()
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()
    
@comment_blueprint.app_errorhandler(400)
def invalid_request(entity):
    message = f"Invalid request ({entity} required)!"
    return jsonify(message), 400

@comment_blueprint.app_errorhandler(400)
def invalid_id(entity=None):
    entity = entity if entity != None else ""
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
    