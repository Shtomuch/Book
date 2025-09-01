from src.domain.services import AuthorService, BookService
from src.infrastructure.repositories import (
    AuthorRepositoryImpl,
    BookRepositoryImpl,
)


async def get_book_service() -> BookService:
    return BookService(
        book_repository=BookRepositoryImpl(),
        author_repository=AuthorRepositoryImpl(),
    )


async def get_author_service() -> AuthorService:
    return AuthorService(author_repository=AuthorRepositoryImpl())