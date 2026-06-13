from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI")
)

db = client["healthcare_ai"]

users_collection = db["users"]
med_collection = db["medications"]
fitness_collection = db["fitness"]
chat_collection = db["chat_history"]
goal_collection = db["fitness_goals"]