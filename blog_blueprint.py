from datetime import datetime

from flask import Blueprint, jsonify, request

from flask_pymongo import PyMongo
import pymongo

from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from bson.json_util import dumps
from bson.objectid import ObjectId
from bson.errors import InvalidId

from config import mongo as mongodb_client


blog_blueprint = Blueprint("blog", import_name=__name__)

@blog_blueprint.route('', methods=['POST'])
def add_blog():
    """
    Add a new blog to the blogs collection
    """
    _json = request.json
    _title = _json['title']
    _text = _json['text']
    _author = _json['author']
    _email = _json['email']
  
    if not _title or len(_title) == 0:  
        return jsonify("Blog title required!"), 400
    elif not _text or len(_text) == 0:  
        return jsonify("Blog body text required!"), 400
    elif not _author:
        return jsonify("Blog author required!"), 400
    
    if len(_title) > 70:
        return jsonify("Blog title should be less than 70 characters!"), 400
    
    _publish = False
    if "publish" in _json:
        _publish = _json["publish"]
    
    _publish_date = None
    if _publish == True:
        _publish_date = datetime.now()
        
    try: 
        author = mongodb_client.db.users.find_one({'email': _email} , {'password': False})
        if author is None:
            return jsonify(f"User with this email does not exist"), 404
        
        mongodb_client.db.blogs.insert_one({'title': _title, 'text': _text, 'author': _author, 'email': _email, 'create_date': datetime.now(), 'publish_date': _publish_date, 'published': _publish, 'update_date': None}) 

        # mongodb_client.db.users.update({'email': _email}, {'$push': {'blogs': blog.inserted_id }})
        
        return jsonify("Blog posted successfully!"), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@blog_blueprint.route('/<id>', methods=['PUT'])
def update_blog(id):
    """
    Update a blog
    """
    _id = id
    _json = request.json
    _title = _json['title']
    _text = _json['text']
    _author = _json['author']
    _email = _json['email']
   
    try:
        author = mongodb_client.db.users.find_one({'email': _email} , {'password': False})
        if author is None:
            return jsonify(f"User with this email does not exist"), 404
        try:
            blog = mongodb_client.db.blogs.find_one({'_id': ObjectId(id)})
        except InvalidId:
            return invalid_id("User")
        
        if blog is None:
            return jsonify("Blog does not exist"), 404
        
        _published = blog['published']
        _publish_date = blog['publish_date']
        
        if "publish" in _json and _json["publish"] != _published:
            _published = _json["publish"]
            if _published == True:
                _publish_date = datetime.now()
            elif _published == False:
               _publish_date = None
            
        mongodb_client.db.blogs.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'title': _title, 'text': _text, 'author': _author, 'email': _email, 'create_date': blog['create_date'], 'publish_date': _publish_date, 'published': _published, 'update_date': datetime.now()}})
        
        return jsonify("Blog updated successfully!"), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@blog_blueprint.route('/<id>', methods=['DELETE'])
def delete_blog(id):
    """
    Delete a blog
    """
    try:
        blog = mongodb_client.db.blogs.delete_one({'_id': ObjectId(id)})
    except InvalidId:
        return invalid_id("Blog")
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()
    
    if blog.deleted_count == 0:
        return jsonify("Blog does not exist"), 404
    return jsonify("Blog deleted successfully"), 200

@blog_blueprint.route('/toggle-publish/<id>', methods=['PATCH'])
def toggle_publish_blog(id):
    """
    Publish/Unpublish a blog
    """
    try:
        try:
            blog = mongodb_client.db.blogs.find_one({'_id': ObjectId(id)})
        except InvalidId:
            return invalid_id("Blog")
        if blog is None:
            return jsonify("Blog does not exist"), 404
    
        if blog['published'] is not None:
            if blog['published'] == True:
                blog['published'] = False
                blog['publish_date'] = None
                mongodb_client.db.blogs.save(blog)
                return jsonify("Blog unpublished successfully"), 200
            else:
                blog['published'] = True
                blog['publish_date'] = datetime.now()
                mongodb_client.db.blogs.save(blog)
                return jsonify("Blog published successfully"), 200
        else:
            blog['published'] = True
            blog['publish_date'] = datetime.now()   
            mongodb_client.db.blogs.save(blog)
            return jsonify("Blog published successfully"), 200       
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@blog_blueprint.route('', methods=['GET'])
def list_blogs():
    """
    List all blogs from the blogs collection
    """
    try:
        blogs = list(mongodb_client.db.blogs.find({}))
        return dumps(blogs), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@blog_blueprint.route('/user/<id>', methods=['GET'])
def list_blogs_by_user(id):
    """
    List all blogs of a user. 
    Set query parameter 'published' to True or False to filter blogs by publish type.
    """
    _published = request.args.get('published')
    if _published != None and (_published not in ("True", "False", "true", "false")):
        return jsonify("Invalid query parameter value for 'published' received"), 400

    try:
        if _published:
            if _published in ("True", "true"):
                blogs = list(mongodb_client.db.blogs.find({'user_id': ObjectId(id), 'published': True}))
            elif _published in ("False", "false"):
                blogs = list(mongodb_client.db.blogs.find({'user_id': ObjectId(id), 'published': False}))
            else:
                blogs = list(mongodb_client.db.blogs.find({'user_id': ObjectId(id)})) 
        else:
            blogs = list(mongodb_client.db.blogs.find({'user_id': ObjectId(id)}))
        return dumps(blogs), 200
    except InvalidId:
        return invalid_id("User")
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()
   
@blog_blueprint.app_errorhandler(400)
def invalid_id(entity):
    message = f"Invalid {entity} Id"
    return jsonify(message), 400

@blog_blueprint.app_errorhandler(404)
def not_found():
    message = "Not Found " + request.url
    return jsonify(message), 404

@blog_blueprint.app_errorhandler(500)
def database_connection_error():
    message = "Unable to connect to the MongoDB server"
    return jsonify(message), 500