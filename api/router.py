from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from schemas.book import Book, BookCreate, BookStatus
from services.book_service import BookService
from uuid import UUID
from typing import List, Optional

router = APIRouter(prefix="/books", tags=["Books"])

# ВАЖЛИВО: Видали тут рядок service = BookService()

@router.get("/", response_model=List[Book])
async def get_books(
    limit: int = Query(10, ge=1, le=100), 
    offset: int = Query(0, ge=0),
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    # Створюємо сервіс прямо тут і передаємо йому сесію БД
    service = BookService(db)
    return await service.list_books(limit, offset, status, author)

@router.get("/{book_id}", response_model=Book)
async def get_one_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.add_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    await service.remove_book(book_id)
    return None