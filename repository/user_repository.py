from motor.motor_asyncio import AsyncIOMotorDatabase

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("users")

    async def get_by_username(self, username: str):
        return await self.collection.find_one({"username": username})

    async def create(self, user_data: dict):
        return await self.collection.insert_one(user_data)