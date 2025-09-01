from datetime import datetime
from typing import List, Optional

from src.domain.entities import Book, Genre
from src.domain.repositories import BookRepository
from src.infrastructure.database import DatabasePool


class BookRepositoryImpl(BookRepository):
    async def create(self, book: Book) -> Book:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO books (title, author_id, genre, published_year, isbn, description)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id, title, author_id, genre, published_year, isbn, description, created_at, updated_at
                """,
                book.title,
                book.author_id,
                book.genre.value,
                book.published_year,
                book.isbn,
                book.description,
            )
            return self._row_to_book(row)

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT id, title, author_id, genre, published_year, isbn, description, created_at, updated_at
                FROM books
                WHERE id = $1
                """,
                book_id,
            )
            return self._row_to_book(row) if row else None

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
        query = """
            SELECT id, title, author_id, genre, published_year, isbn, description, created_at, updated_at
            FROM books
            WHERE 1=1
        """
        params = []
        param_count = 0

        if title:
            param_count += 1
            query += f" AND LOWER(title) LIKE LOWER(${param_count})"
            params.append(f"%{title}%")

        if author_id:
            param_count += 1
            query += f" AND author_id = ${param_count}"
            params.append(author_id)

        if genre:
            param_count += 1
            query += f" AND genre = ${param_count}"
            params.append(genre)

        if year_from:
            param_count += 1
            query += f" AND published_year >= ${param_count}"
            params.append(year_from)

        if year_to:
            param_count += 1
            query += f" AND published_year <= ${param_count}"
            params.append(year_to)

        valid_sort_fields = {"title", "published_year", "created_at", "updated_at"}
        if sort_by and sort_by in valid_sort_fields:
            query += f" ORDER BY {sort_by} {order.upper()}"
        else:
            query += " ORDER BY created_at DESC"

        param_count += 1
        query += f" LIMIT ${param_count}"
        params.append(limit)

        param_count += 1
        query += f" OFFSET ${param_count}"
        params.append(offset)

        async with DatabasePool.acquire() as connection:
            rows = await connection.fetch(query, *params)
            return [self._row_to_book(row) for row in rows]

    async def update(self, book_id: int, book: Book) -> Optional[Book]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                UPDATE books
                SET title = $2, author_id = $3, genre = $4, published_year = $5, isbn = $6, description = $7
                WHERE id = $1
                RETURNING id, title, author_id, genre, published_year, isbn, description, created_at, updated_at
                """,
                book_id,
                book.title,
                book.author_id,
                book.genre.value,
                book.published_year,
                book.isbn,
                book.description,
            )
            return self._row_to_book(row) if row else None

    async def delete(self, book_id: int) -> bool:
        async with DatabasePool.acquire() as connection:
            result = await connection.execute(
                "DELETE FROM books WHERE id = $1",
                book_id,
            )
            return result != "DELETE 0"

    async def count(
        self,
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        genre: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> int:
        query = "SELECT COUNT(*) FROM books WHERE 1=1"
        params = []
        param_count = 0

        if title:
            param_count += 1
            query += f" AND LOWER(title) LIKE LOWER(${param_count})"
            params.append(f"%{title}%")

        if author_id:
            param_count += 1
            query += f" AND author_id = ${param_count}"
            params.append(author_id)

        if genre:
            param_count += 1
            query += f" AND genre = ${param_count}"
            params.append(genre)

        if year_from:
            param_count += 1
            query += f" AND published_year >= ${param_count}"
            params.append(year_from)

        if year_to:
            param_count += 1
            query += f" AND published_year <= ${param_count}"
            params.append(year_to)

        async with DatabasePool.acquire() as connection:
            count = await connection.fetchval(query, *params)
            return count or 0

    async def bulk_create(self, books: List[Book]) -> List[Book]:
        async with DatabasePool.transaction() as connection:
            values = [
                (b.title, b.author_id, b.genre.value, b.published_year, b.isbn, b.description)
                for b in books
            ]
            
            rows = await connection.fetch(
                """
                INSERT INTO books (title, author_id, genre, published_year, isbn, description)
                SELECT * FROM UNNEST($1::text[], $2::int[], $3::text[], $4::int[], $5::text[], $6::text[])
                RETURNING id, title, author_id, genre, published_year, isbn, description, created_at, updated_at
                """,
                [v[0] for v in values],
                [v[1] for v in values],
                [v[2] for v in values],
                [v[3] for v in values],
                [v[4] for v in values],
                [v[5] for v in values],
            )
            return [self._row_to_book(row) for row in rows]

    async def get_by_isbn(self, isbn: str) -> Optional[Book]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT id, title, author_id, genre, published_year, isbn, description, created_at, updated_at
                FROM books
                WHERE isbn = $1
                """,
                isbn,
            )
            return self._row_to_book(row) if row else None

    @staticmethod
    def _row_to_book(row) -> Book:
        return Book(
            id=row["id"],
            title=row["title"],
            author_id=row["author_id"],
            genre=Genre(row["genre"]),
            published_year=row["published_year"],
            isbn=row["isbn"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )