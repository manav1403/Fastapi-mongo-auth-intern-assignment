from pymongo import MongoClient



client = MongoClient("mongodb://localhost:27017")


db = client.todo_app
user_db = db["users"]

collection_name = db["todos_app"]
