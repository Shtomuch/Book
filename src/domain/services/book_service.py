from datetime import datetime
from typing import List, Optional

from src.core.exceptions import ConflictException, NotFoundException, ValidationException
from src.domain.entities import Book
from src.domain.repositories import AuthorRepository, BookRepository


class BookService:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository = book_repository
        self.author_repository = author_repository

    async def create_book(self, book: Book) -> Book:
        await self._validate_book(book)
        
        if book.isbn:
            existing = await self.book_repository.get_by_isbn(book.isbn)
            if existing:
                raise ConflictException(f"Book with ISBN {book.isbn} already exists")
        
        return await self.book_repository.create(book)

    async def get_book(self, book_id: int) -> Book:
        book = await self.book_repository.get_by_id(book_id)
        if not book:
            raise NotFoundException("Book", book_id)
        return book

    async def get_books(
        self,
        page: int = 1,
        size: int = 50,
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        genre: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: str = "asc",
    ) -> dict:
        offset = (page - 1) * size
        
        books = await self.book_repository.get_all(
            limit=size,
            offset=offset,
            title=title,
            author_id=author_id,
            genre=genre,
            year_from=year_from,
            year_to=year_to,
            sort_by=sort_by,
            order=order,
        )
        
        total = await self.book_repository.count(
            title=title,
            author_id=author_id,
            genre=genre,
            year_from=year_from,
            year_to=year_to,
        )
        
        return {
            "items": books,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size,
        }

    async def update_book(self, book_id: int, book: Book) -> Book:
        existing = await self.book_repository.get_by_id(book_id)
        if not existing:
            raise NotFoundException("Book", book_id)
        
        await self._validate_book(book)
        
        if book.isbn and book.isbn != existing.isbn:
            isbn_book = await self.book_repository.get_by_isbn(book.isbn)
            if isbn_book and isbn_book.id != book_id:
                raise ConflictException(f"Book with ISBN {book.isbn} already exists")
        
        updated = await self.book_repository.update(book_id, book)
        if not updated:
            raise NotFoundException("Book", book_id)
        return updated

    async def delete_book(self, book_id: int) -> None:
        deleted = await self.book_repository.delete(book_id)
        if not deleted:
            raise NotFoundException("Book", book_id)

    async def bulk_create_books(self, books: List[Book]) -> List[Book]:
        for book in books:
            await self._validate_book(book)
        
        isbn_list = [b.isbn for b in books if b.isbn]
        if len(isbn_list) != len(set(isbn_list)):
            raise ValidationException("Duplicate ISBNs in bulk import")
        
        for isbn in isbn_list:
            existing = await self.book_repository.get_by_isbn(isbn)
            if existing:
                raise ConflictException(f"Book with ISBN {isbn} already exists")
        
        return await self.book_repository.bulk_create(books)

    async def _validate_book(self, book: Book) -> None:
        if not book.title or not book.title.strip():
            raise ValidationException("Book title cannot be empty")
        
        author = await self.author_repository.get_by_id(book.author_id)
        if not author:
            raise ValidationException(f"Author with id {book.author_id} does not exist")
        
        current_year = datetime.now().year
        if book.published_year < 1800 or book.published_year > current_year:
            raise ValidationException(
                f"Published year must be between 1800 and {current_year}"
            )