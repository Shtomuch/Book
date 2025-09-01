import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from src.infrastructure.database import DatabasePool
from src.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_database():
    await DatabasePool.initialize()
    yield
    await DatabasePool.close()


@pytest.fixture
async def client(setup_database) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def authenticated_client(client: AsyncClient) -> AsyncClient:
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123",
    }
    await client.post("/api/v1/auth/register", json=register_data)
    
    login_data = {
        "username": "testuser",
        "password": "TestPass123",
    }
    response = await client.post(
        "/api/v1/auth/login",
        data=login_data,
    )
    token = response.json()["access_token"]
    
    client.headers["Authorization"] = f"Bearer {token}"
    return client