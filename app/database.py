from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["ecommerce_db"]

products_collection = db["products"]
orders_collection = db["orders"]

# Indexes
products_collection.create_index([("name", ASCENDING)])
