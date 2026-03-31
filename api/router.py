from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from schemas.book import Book, BookCreate, BookCursorPaginationResponse, decode_cursor
from repository.book_repository import BookRepository
from typing import Optional

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=BookCursorPaginationResponse)
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    decoded_id = decode_cursor(cursor) if cursor else None
    repo = BookRepository(db)
    items, next_cursor = await repo.get_all_cursor(limit, decoded_id)
    return {"items": items, "next_cursor": next_cursor}

@router.post("/", response_model=Book)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    return await repo.create(book)