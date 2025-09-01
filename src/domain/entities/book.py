from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Genre(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    BIOGRAPHY = "Biography"
    FANTASY = "Fantasy"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    POETRY = "Poetry"


@dataclass
class Book:
    id: Optional[int]
    title: str
    author_id: int
    genre: Genre
    published_year: int
    isbn: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]