from flask_pymongo import PyMongo
from pymongo import MongoClient

print("SCRIPT START")

client = MongoClient(f"mongodb+srv://user:user_mongo020@cluster0.ovq4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

print("MONGO CONNECT")
print(client)
