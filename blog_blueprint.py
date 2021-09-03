from datetime import datetime

from flask import Blueprint, jsonify, request

from flask_pymongo import PyMongo
import pymongo

from pymongo.errors import ConnectionFailure, DuplicateKeyError, ServerSelectionTimeoutError, OperationFailure

from bson.json_util import dumps
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash

from config import mongo as mongodb_client


blog_blueprint = Blueprint("blog", import_name=__name__)


@blog_blueprint.route('')
def list_blogs():
    """
    List all blogs from the blogs collection
    """
    try:
        blogs = list(mongodb_client.db.blogs.find({} , {'password': False}))
        return dumps(blogs), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@blog_blueprint.app_errorhandler(404)
def not_found():
    message = 'Not Found ' + request.url
    return jsonify(message), 404

@blog_blueprint.app_errorhandler(500)
def database_connection_error():
    message = 'Unable to connect to the MongoDB server'
    return jsonify(message), 500

