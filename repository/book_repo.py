from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.book import BookModel
from uuid import UUID

class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, limit: int, offset: int, status=None, author=None):
        query = select(BookModel).offset(offset).limit(limit)
        
        if status:
            query = query.where(BookModel.status == status)
        if author:
            query = query.where(BookModel.author.ilike(f"%{author}%"))
            
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, book_data):
        new_book = BookModel(**book_data.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def delete(self, book_id: UUID):
        query = delete(BookModel).where(BookModel.id == book_id)
        await self.session.execute(query)
        await self.session.commit()