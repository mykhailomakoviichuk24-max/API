from sqlalchemy.ext.asyncio import AsyncSession
from repository.book_repo import BookRepository
from schemas.book import BookStatus
from typing import Optional

class BookService:
    
    def __init__(self, db: AsyncSession):
        self.repo = BookRepository(db)

    async def list_books(self, limit: int, offset: int, 
                         status: Optional[BookStatus] = None, 
                         author: Optional[str] = None):
        return await self.repo.get_all(limit, offset, status, author)

    async def get_book(self, book_id):
        return await self.repo.get_by_id(book_id)

    async def add_book(self, book_data):
        return await self.repo.create(book_data)

    async def remove_book(self, book_id):
        await self.repo.delete(book_id)