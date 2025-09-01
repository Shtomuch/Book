from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import Author


class AuthorRepository(ABC):
    @abstractmethod
    async def create(self, author: Author) -> Author:
        pass

    @abstractmethod
    async def get_by_id(self, author_id: int) -> Optional[Author]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Author]:
        pass

    @abstractmethod
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        name: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> List[Author]:
        pass

    @abstractmethod
    async def update(self, author_id: int, author: Author) -> Optional[Author]:
        pass

    @abstractmethod
    async def delete(self, author_id: int) -> bool:
        pass

    @abstractmethod
    async def count(
        self,
        name: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> int:
        pass