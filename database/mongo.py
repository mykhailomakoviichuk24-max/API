import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://user:pass@localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
database = client.library_db

def get_db():
    return database