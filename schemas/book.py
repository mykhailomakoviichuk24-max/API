from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from typing import Optional


class BookStatus(str, Enum):
    AVAILABLE = "наявна"
    BORROWED = "видана"


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    release_year: int = Field(..., gt=0, lt=2100)
    status: BookStatus = BookStatus.AVAILABLE


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: UUID