import base64
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID
from enum import Enum

class BookStatus(str, Enum):
    AVAILABLE = "наявна"
    BORROWED = "видана"

def encode_cursor(cursor_id: UUID) -> str:
    return base64.b64encode(str(cursor_id).encode()).decode()

def decode_cursor(cursor_str: str) -> UUID:
    return UUID(base64.b64decode(cursor_str.encode()).decode())

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    release_year: int = Field(..., gt=0)
    status: BookStatus = BookStatus.AVAILABLE

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class BookCursorPaginationResponse(BaseModel):
    items: List[Book]
    next_cursor: Optional[str] = None