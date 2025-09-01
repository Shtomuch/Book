from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import Book


class BookRepository(ABC):
    @abstractmethod
    async def create(self, book: Book) -> Book:
        pass

    @abstractmethod
    async def get_by_id(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        genre: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: str = "asc",
    ) -> List[Book]:
        pass

    @abstractmethod
    async def update(self, book_id: int, book: Book) -> Optional[Book]:
        pass

    @abstractmethod
    async def delete(self, book_id: int) -> bool:
        pass

    @abstractmethod
    async def count(
        self,
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        genre: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> int:
        pass

    @abstractmethod
    async def bulk_create(self, books: List[Book]) -> List[Book]:
        pass

    @abstractmethod
    async def get_by_isbn(self, isbn: str) -> Optional[Book]:
        pass