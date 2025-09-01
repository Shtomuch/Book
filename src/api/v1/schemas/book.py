from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.domain.entities import Genre


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author_id: int = Field(..., gt=0)
    genre: Genre
    published_year: int = Field(..., ge=1800, le=2100)
    isbn: Optional[str] = Field(None, max_length=20, pattern=r"^[\d-]*$")
    description: Optional[str] = Field(None, max_length=5000)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()

    @field_validator("published_year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError(f"Published year cannot be greater than {current_year}")
        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookPagination(BaseModel):
    items: list[BookResponse]
    total: int
    page: int
    size: int
    pages: int


class BookBulkCreate(BaseModel):
    books: list[BookCreate]