from sqlalchemy import select, asc
from models.book import BookModel
from uuid import UUID
from typing import Optional
from schemas.book import encode_cursor

class BookRepository:
    def __init__(self, session):
        self.session = session

    async def get_all_cursor(self, limit: int, cursor: Optional[UUID] = None):
        # Отримуємо на 1 елемент більше, щоб дізнатися, чи є наступна сторінка
        query = select(BookModel).order_by(asc(BookModel.id)).limit(limit + 1)
        
        if cursor:
            query = query.where(BookModel.id > cursor)
            
        result = await self.session.execute(query)
        items = list(result.scalars().all())
        
        next_cursor = None
        if len(items) > limit:
            next_cursor = encode_cursor(items[limit-1].id)
            items = items[:limit]
            
        return items, next_cursor

    async def create(self, data):
        book = BookModel(**data.model_dump())
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book