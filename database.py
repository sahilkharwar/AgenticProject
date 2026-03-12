from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["healthcare_ai"]

users_collection = db["users"]
med_collection = db["medications"]
fitness_collection = db["fitness"]