import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "SecurePass123",
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "SecurePass123",
    }
    
    await client.post("/api/v1/auth/register", json=user_data)
    
    user_data["username"] = "user2"
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_invalid_password(client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "weak",
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "SecurePass123",
    }
    
    await client.post("/api/v1/auth/register", json=user_data)
    
    login_data = {
        "username": "loginuser",
        "password": "SecurePass123",
    }
    
    response = await client.post(
        "/api/v1/auth/login",
        data=login_data,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    login_data = {
        "username": "nonexistent",
        "password": "WrongPass123",
    }
    
    response = await client.post(
        "/api/v1/auth/login",
        data=login_data,
    )
    
    assert response.status_code == 401