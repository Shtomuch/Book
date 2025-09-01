from typing import Optional

from src.domain.entities import User
from src.domain.repositories import UserRepository
from src.infrastructure.database import DatabasePool


class UserRepositoryImpl(UserRepository):
    async def create(self, user: User) -> User:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO users (email, username, hashed_password, is_active, is_superuser)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, email, username, hashed_password, is_active, is_superuser, created_at, updated_at
                """,
                user.email,
                user.username,
                user.hashed_password,
                user.is_active,
                user.is_superuser,
            )
            return self._row_to_user(row)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT id, email, username, hashed_password, is_active, is_superuser, created_at, updated_at
                FROM users
                WHERE id = $1
                """,
                user_id,
            )
            return self._row_to_user(row) if row else None

    async def get_by_email(self, email: str) -> Optional[User]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT id, email, username, hashed_password, is_active, is_superuser, created_at, updated_at
                FROM users
                WHERE LOWER(email) = LOWER($1)
                """,
                email,
            )
            return self._row_to_user(row) if row else None

    async def get_by_username(self, username: str) -> Optional[User]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT id, email, username, hashed_password, is_active, is_superuser, created_at, updated_at
                FROM users
                WHERE LOWER(username) = LOWER($1)
                """,
                username,
            )
            return self._row_to_user(row) if row else None

    async def update(self, user_id: int, user: User) -> Optional[User]:
        async with DatabasePool.acquire() as connection:
            row = await connection.fetchrow(
                """
                UPDATE users
                SET email = $2, username = $3, hashed_password = $4, is_active = $5, is_superuser = $6
                WHERE id = $1
                RETURNING id, email, username, hashed_password, is_active, is_superuser, created_at, updated_at
                """,
                user_id,
                user.email,
                user.username,
                user.hashed_password,
                user.is_active,
                user.is_superuser,
            )
            return self._row_to_user(row) if row else None

    async def delete(self, user_id: int) -> bool:
        async with DatabasePool.acquire() as connection:
            result = await connection.execute(
                "DELETE FROM users WHERE id = $1",
                user_id,
            )
            return result != "DELETE 0"

    @staticmethod
    def _row_to_user(row) -> User:
        return User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            hashed_password=row["hashed_password"],
            is_active=row["is_active"],
            is_superuser=row["is_superuser"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )