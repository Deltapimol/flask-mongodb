from flask_pymongo import PyMongo
mongo = PyMongo() 

class MongoClass:
    
    def __init__(self):
        self.MONGO_USER = "user"
        self.MONGO_PASSWORD = "user_mongo020"
        self.MONGO_DATABASE = "myFirstDatabase"
    
    def get_mongo_uri(self):
        return f"mongodb+srv://{self.MONGO_USER}:{self.MONGO_PASSWORD}@cluster0.ovq4g.mongodb.net/{self.MONGO_DATABASE}?retryWrites=true&w=majority"


    
        