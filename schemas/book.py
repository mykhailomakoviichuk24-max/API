from pydantic import BaseModel, Field, ConfigDict
from typing import List, Any
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

# Валідатор для перетворення ObjectId від MongoDB у звичайний рядок
def check_object_id(v: Any) -> str:
    return str(v)

PyObjectId = Annotated[str, AfterValidator(check_object_id)]

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    release_year: int = Field(..., gt=0)

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: PyObjectId = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)

class BookPaginationResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[BookResponse]