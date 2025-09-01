import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_book_unauthorized(client: AsyncClient):
    book_data = {
        "title": "Test Book",
        "author_id": 1,
        "genre": "Fiction",
        "published_year": 2023,
        "isbn": "978-0-123456-78-9",
        "description": "A test book",
    }
    
    response = await client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_books(client: AsyncClient):
    response = await client.get("/api/v1/books/")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data


@pytest.mark.asyncio
async def test_get_books_with_pagination(client: AsyncClient):
    response = await client.get("/api/v1/books/?page=1&size=10")
    
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 10
    assert len(data["items"]) <= 10


@pytest.mark.asyncio
async def test_get_books_with_filters(client: AsyncClient):
    response = await client.get("/api/v1/books/?genre=Fiction&year_from=2020&year_to=2024")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_get_book_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/v1/books/99999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_bulk_import_books_unauthorized(client: AsyncClient):
    bulk_data = {
        "books": [
            {
                "title": "Book 1",
                "author_id": 1,
                "genre": "Fiction",
                "published_year": 2023,
            },
            {
                "title": "Book 2",
                "author_id": 1,
                "genre": "Science",
                "published_year": 2022,
            },
        ]
    }
    
    response = await client.post("/api/v1/books/bulk", json=bulk_data)
    assert response.status_code == 403