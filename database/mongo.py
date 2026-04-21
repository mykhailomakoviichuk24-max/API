import os
from motor.motor_asyncio import AsyncIOMotorClient

# URL береться з docker-compose.yml, або використовується локальний за замовчуванням
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

client = AsyncIOMotorClient(MONGO_URL)
database = client.library_db

# Ця функція потрібна для Depends(get_db) у роутерах
def get_db():
    return database