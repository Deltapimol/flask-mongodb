from datetime import datetime

from flask import Flask, jsonify, request

from flask_pymongo import PyMongo
import pymongo

from pymongo.errors import ConnectionFailure, DuplicateKeyError, ServerSelectionTimeoutError, OperationFailure

from bson.json_util import dumps
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash

from config import MongoClass


app = Flask(__name__)

app.secret_key = "ZLFdHXIUeekwJCu"

MONGO_CRED = MongoClass()

app.config["MONGO_URI"] = f"mongodb+srv://{MONGO_CRED.MONGO_USER}:{MONGO_CRED.MONGO_PASSWORD}@cluster0.ovq4g.mongodb.net/{MONGO_CRED.MONGO_DATABASE}?retryWrites=true&w=majority"

mongodb_client = PyMongo(app)


@app.route('/user', methods=['POST'])
def add_user():
    """
    Add a new user to the collection
    """
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']
    
    if _name and _email and _password and request.method == 'POST':
        try:
            _hashed_password = generate_password_hash(_password)
            id = mongodb_client.db.users.insert({'name':_name, 'email':_email, 'password':_hashed_password, 'create_date': datetime.now(), 'update_date': None})

            return jsonify(f"User '{_name}' created successfully!"), 200
        except DuplicateKeyError:
            return email_already_exists()
        except (ServerSelectionTimeoutError, ConnectionFailure):
            return database_connection_error()
    else:
        return not_found()

@app.route('/users', methods=['GET'])
def list_users():
    """
    List all users from the user collection
    """
    try:
        users = list(mongodb_client.db.users.find({} , {'password': False}))
        return dumps(users), 200
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()

@app.route('/user/<id>', methods=['GET'])
def user(id):
    """
    Fetch specific user details
    """
    try:
        user = mongodb_client.db.users.find_one({'_id':ObjectId(id)}, {'password': False})
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()
    
    if user is None:
        return jsonify("User does not exist"), 404
    return dumps(user), 200

@app.route('/user/<id>', methods=['DELETE'])
def delete(id):
    """
    Delete specific user details
    """
    try:
        user = mongodb_client.db.users.delete_one({'_id':ObjectId(id)})
    except (ServerSelectionTimeoutError, ConnectionFailure):
        return database_connection_error()
    
    if user.deleted_count == 0:
        return jsonify("User does not exist"), 404
    return jsonify("User details deleted successfully"), 200

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    """
    Update user details
    """
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and request.method == 'PUT':
        try:
            _hashed_password = generate_password_hash(_password)
            user = mongodb_client.db.users.find_one({'_id':ObjectId(id)}, {'password': False})
            if user is None:
                return jsonify("User does not exist"), 404
            _create_date = datetime.now()
            if "create_date" in user:
                _create_date = user["create_date"]
            updated_user = mongodb_client.db.users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'password': _hashed_password, 'create_date': _create_date, 'update_date': datetime.now()}})

            return jsonify(f"User updated successfully!"), 200
        except DuplicateKeyError:
            return email_already_exists()
        except (ServerSelectionTimeoutError, ConnectionFailure):
            return database_connection_error()
    else:
        return not_found() 
    
@app.errorhandler(404)
def not_found():
    message = 'Not Found ' + request.url
    return jsonify(message), 404

@app.errorhandler(409)
def email_already_exists():
    message = 'Conflict. User with this email address already exists.'
    return jsonify(message), 409

@app.errorhandler(500)
def database_connection_error():
    message = 'Unable to connect to the MongoDB server'
    return jsonify(message), 500
          
                 
if __name__ == "__main__":
    with app.app_context():
        try:
            mongodb_client.db.users.create_index([("email", pymongo.ASCENDING),], unique=True)
        except (ServerSelectionTimeoutError,ConnectionFailure) as ex:
            print(ex)
    app.run(debug=True)