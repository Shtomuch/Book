import pytest

from src.core.exceptions import ConflictException, NotFoundException, ValidationException
from src.domain.entities import Author, Book, Genre
from src.domain.services import AuthorService, AuthService, BookService
from src.infrastructure.repositories import (
    AuthorRepositoryImpl,
    BookRepositoryImpl,
    UserRepositoryImpl,
)


@pytest.mark.asyncio
async def test_book_service_validation():
    book_service = BookService(
        book_repository=BookRepositoryImpl(),
        author_repository=AuthorRepositoryImpl(),
    )
    
    invalid_book = Book(
        id=None,
        title="",
        author_id=99999,
        genre=Genre.FICTION,
        published_year=2023,
        isbn=None,
        description=None,
        created_at=None,
        updated_at=None,
    )
    
    with pytest.raises(ValidationException):
        await book_service.create_book(invalid_book)


@pytest.mark.asyncio
async def test_author_service_validation():
    author_service = AuthorService(author_repository=AuthorRepositoryImpl())
    
    invalid_author = Author(
        id=None,
        name="",
        biography=None,
        birth_year=3000,
        nationality=None,
        created_at=None,
        updated_at=None,
    )
    
    with pytest.raises(ValidationException):
        await author_service.create_author(invalid_author)


@pytest.mark.asyncio
async def test_auth_service_password_validation():
    auth_service = AuthService(user_repository=UserRepositoryImpl())
    
    with pytest.raises(ValidationException) as exc_info:
        await auth_service.register(
            email="test@example.com",
            username="testuser",
            password="weak",
        )
    
    assert "at least 8 characters" in str(exc_info.value)