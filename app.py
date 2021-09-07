from flask import Flask

import pymongo

from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from flask_cors import CORS

from config import mongo, MongoClass

from user_blueprint import user_blueprint
from blog_blueprint import blog_blueprint
from comment_blueprint import comment_blueprint


app = Flask(__name__)

CORS(app)

app.secret_key = "ZLFdHXIUeekwJCu"

# MongoDB configuration
app.config.from_object('config')
app.config["MONGO_URI"] = MongoClass().get_mongo_uri()

mongo.init_app(app)

# Blueprints
URL_PREFIX = '/api/v1'
app.register_blueprint(user_blueprint, url_prefix=f'{URL_PREFIX}/users')
app.register_blueprint(blog_blueprint, url_prefix=f'{URL_PREFIX}/blogs')
app.register_blueprint(comment_blueprint, url_prefix=f'{URL_PREFIX}/comments')

               
if __name__ == "__main__":
    with app.app_context():
        try:
            mongo.db.users.create_index([("email", pymongo.ASCENDING),], unique=True)
        except (ServerSelectionTimeoutError, ConnectionFailure) as ex:
            print(ex)
    app.run(debug=True, port=5000)