import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGODB_URI is missing. Check your .env file.")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["flask_mongodb_db"]
submissions_collection = db["submissions"]