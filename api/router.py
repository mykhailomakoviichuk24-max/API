from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase  # <--- Тепер імпортується правильно
from database.mongo import get_db                     # <--- Твоя функція з mongo.py
from repository.book_repository import BookRepository
from schemas.book import BookResponse, BookCreate, BookPaginationResponse

router = APIRouter(prefix="/books", tags=["Books"])

def get_book_repository(db: AsyncIOMotorDatabase = Depends(get_db)):
    return BookRepository(db)

@router.get("/", response_model=BookPaginationResponse)
async def list_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo: BookRepository = Depends(get_book_repository)
):
    items, total = await repo.get_all(limit, offset)
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }

@router.post("/", response_model=BookResponse)
async def create_book(
    book: BookCreate, 
    repo: BookRepository = Depends(get_book_repository)
):
    return await repo.create(book)