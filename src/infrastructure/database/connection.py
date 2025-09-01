from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from asyncpg import Connection, Pool

from src.core.config import settings


class DatabasePool:
    _instance: Pool | None = None

    @classmethod
    async def initialize(cls) -> None:
        if cls._instance is None:
            cls._instance = await asyncpg.create_pool(
                str(settings.database_url.unicode_string()),
                min_size=10,
                max_size=20,
                command_timeout=60,
            )

    @classmethod
    async def close(cls) -> None:
        if cls._instance:
            await cls._instance.close()
            cls._instance = None

    @classmethod
    @asynccontextmanager
    async def acquire(cls) -> AsyncGenerator[Connection, None]:
        if cls._instance is None:
            await cls.initialize()
        async with cls._instance.acquire() as connection:
            yield connection

    @classmethod
    @asynccontextmanager
    async def transaction(cls) -> AsyncGenerator[Connection, None]:
        async with cls.acquire() as connection:
            async with connection.transaction():
                yield connection