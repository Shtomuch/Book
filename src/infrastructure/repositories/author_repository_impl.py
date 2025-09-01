from typing import List, Optional

from src.domain.entities import Author
from src.domain.repositories import AuthorRepository
from src.infrastructure.database import DatabasePool


class AuthorRepositoryImpl(AuthorRepository):
    async def create(self, author: Author) -> Author:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO authors (name, biography, birth_year, nationality)
                VALUES ($1, $2, $3, $4)
                RETURNING id, name, biography, birth_year, nationality, created_at, updated_at
                """,
                author.name,
                author.biography,
                author.birth_year,
                author.nationality,
            )
            return self._row_to_author(row)

    async def get_by_id(self, author_id: int) -> Optional[Author]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT id, name, biography, birth_year, nationality, created_at, updated_at
                FROM authors
                WHERE id = $1
                """,
                author_id,
            )
            return self._row_to_author(row) if row else None

    async def get_by_name(self, name: str) -> Optional[Author]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT id, name, biography, birth_year, nationality, created_at, updated_at
                FROM authors
                WHERE LOWER(name) = LOWER($1)
                """,
                name,
            )
            return self._row_to_author(row) if row else None

    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        name: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> List[Author]:
        query = """
            SELECT id, name, biography, birth_year, nationality, created_at, updated_at
            FROM authors
            WHERE 1=1
        """
        params = []
        param_count = 0

        if name:
            param_count += 1
            query += f" AND LOWER(name) LIKE LOWER(${param_count})"
            params.append(f"%{name}%")

        if nationality:
            param_count += 1
            query += f" AND LOWER(nationality) LIKE LOWER(${param_count})"
            params.append(f"%{nationality}%")

        query += " ORDER BY name ASC"

        param_count += 1
        query += f" LIMIT ${param_count}"
        params.append(limit)

        param_count += 1
        query += f" OFFSET ${param_count}"
        params.append(offset)

        async with DatabasePool.acquire() as connection:
            rows = await connection.fetch(query, *params)
            return [self._row_to_author(row) for row in rows]

    async def update(self, author_id: int, author: Author) -> Optional[Author]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                UPDATE authors
                SET name = $2, biography = $3, birth_year = $4, nationality = $5
                WHERE id = $1
                RETURNING id, name, biography, birth_year, nationality, created_at, updated_at
                """,
                author_id,
                author.name,
                author.biography,
                author.birth_year,
                author.nationality,
            )
            return self._row_to_author(row) if row else None

    async def delete(self, author_id: int) -> bool:
        async with DatabasePool.acquire() as connection:
            result = await connection.execute(
                "DELETE FROM authors WHERE id = $1",
                author_id,
            )
            return result != "DELETE 0"

    async def count(
        self,
        name: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> int:
        query = "SELECT COUNT(*) FROM authors WHERE 1=1"
        params = []
        param_count = 0

        if name:
            param_count += 1
            query += f" AND LOWER(name) LIKE LOWER(${param_count})"
            params.append(f"%{name}%")

        if nationality:
            param_count += 1
            query += f" AND LOWER(nationality) LIKE LOWER(${param_count})"
            params.append(f"%{nationality}%")

        async with DatabasePool.acquire() as connection:
            count = await connection.fetchval(query, *params)
            return count or 0

    @staticmethod
    def _row_to_author(row) -> Author:
        return Author(
            id=row["id"],
            name=row["name"],
            biography=row["biography"],
            birth_year=row["birth_year"],
            nationality=row["nationality"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )