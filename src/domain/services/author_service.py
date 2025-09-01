from typing import Optional

from src.core.exceptions import ConflictException, NotFoundException, ValidationException
from src.domain.entities import Author
from src.domain.repositories import AuthorRepository


class AuthorService:
    def __init__(self, author_repository: AuthorRepository):
        self.author_repository = author_repository

    async def create_author(self, author: Author) -> Author:
        await self._validate_author(author)
        
        existing = await self.author_repository.get_by_name(author.name)
        if existing:
            raise ConflictException(f"Author with name '{author.name}' already exists")
        
        return await self.author_repository.create(author)

    async def get_author(self, author_id: int) -> Author:
        author = await self.author_repository.get_by_id(author_id)
        if not author:
            raise NotFoundException("Author", author_id)
        return author

    async def get_authors(
        self,
        page: int = 1,
        size: int = 50,
        name: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> dict:
        offset = (page - 1) * size
        
        authors = await self.author_repository.get_all(
            limit=size,
            offset=offset,
            name=name,
            nationality=nationality,
        )
        
        total = await self.author_repository.count(
            name=name,
            nationality=nationality,
        )
        
        return {
            "items": authors,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size,
        }

    async def update_author(self, author_id: int, author: Author) -> Author:
        existing = await self.author_repository.get_by_id(author_id)
        if not existing:
            raise NotFoundException("Author", author_id)
        
        await self._validate_author(author)
        
        if author.name != existing.name:
            name_exists = await self.author_repository.get_by_name(author.name)
            if name_exists:
                raise ConflictException(f"Author with name '{author.name}' already exists")
        
        updated = await self.author_repository.update(author_id, author)
        if not updated:
            raise NotFoundException("Author", author_id)
        return updated

    async def delete_author(self, author_id: int) -> None:
        deleted = await self.author_repository.delete(author_id)
        if not deleted:
            raise NotFoundException("Author", author_id)

    async def _validate_author(self, author: Author) -> None:
        if not author.name or not author.name.strip():
            raise ValidationException("Author name cannot be empty")
        
        if author.birth_year:
            from datetime import datetime
            current_year = datetime.now().year
            if author.birth_year < 1000 or author.birth_year > current_year:
                raise ValidationException(
                    f"Birth year must be between 1000 and {current_year}"
                )