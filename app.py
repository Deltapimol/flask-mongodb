from flask import Flask, json, jsonify, request, make_response

from flask_pymongo import PyMongo

from bson.json_util import dumps
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = "ZLFdHXIUeekwJCu"

app.config["MONGO_URI"] = "mongodb+srv://user:user_mongo020@cluster0.ovq4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_user():
    print("REQUESTED API")
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']
    print("EMAIL", _email)
    if _name and _email and _password and request.method == 'POST':
        
        try:
            db_check = mongo.db.user.find({"email":_email})
            print("DB CHECK", db_check)
            print("LIST", list(db_check))
            if db_check.count != 0:
                return make_response(jsonify("User with this email already exists"), 400)
            else:
                _hashed_password = generate_password_hash(_password)
                id = mongo.db.user.insert({'name':_name, 'email':_email, 'password':_hashed_password})
                # resp = jsonify(f"User '{_name}' created successfully!")
                # resp.status_code = 200
               
                return make_response(jsonify(f"User '{_name}' created successfully!"), 200)  
            
        except Exception as ex:
            return make_response(jsonify(ex), 500)  
        
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = 'Not Found' + request.url
    resp = make_response(jsonify(message), 404)

    return resp
                 
if __name__ == "__main__":
    app.run(debug=True)