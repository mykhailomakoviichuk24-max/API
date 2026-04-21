from fastapi import APIRouter, Depends, Query, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database.mongo import get_db
from repository.book_repository import BookRepository
from schemas.book import BookResponse, BookCreate, BookPaginationResponse
from api.deps import get_current_user  # Імпортуємо наш захист

router = APIRouter(prefix="/books", tags=["Books"])

# Допоміжна функція для отримання репозиторію
def get_book_repository(db: AsyncIOMotorDatabase = Depends(get_db)):
    return BookRepository(db)

@router.get("/", response_model=BookPaginationResponse)
async def list_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo: BookRepository = Depends(get_book_repository),
    current_user: str = Depends(get_current_user) # Захист активовано
):
    """
    Отримати список книг із пагінацією.
    Доступно лише авторизованим користувачам.
    """
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
    repo: BookRepository = Depends(get_book_repository),
    current_user: str = Depends(get_current_user) # Захист активовано
):
    """
    Додати нову книгу в базу.
    Доступно лише авторизованим користувачам.
    """
    return await repo.create(book)

# Додатково: отримання однієї книги за ID (також під захистом)
@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    repo: BookRepository = Depends(get_book_repository),
    current_user: str = Depends(get_current_user)
):
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book