from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.book import BookCreate
from bson import ObjectId

class BookRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        # Працюємо з колекцією "books"
        self.collection = db.get_collection("books")

    async def get_all(self, limit: int, offset: int):
        """Отримати всі книги з пагінацією"""
        cursor = self.collection.find().skip(offset).limit(limit)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents({})
        return items, total

    async def get_by_id(self, id: str):
        """Знайти одну книгу за ID"""
        if not ObjectId.is_valid(id):
            return None
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def create(self, book_data: BookCreate):
        """Створити нову книгу"""
        new_book = await self.collection.insert_one(book_data.model_dump())
        created_book = await self.collection.find_one({"_id": new_book.inserted_id})
        return created_book