import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_authors(client: AsyncClient):
    response = await client.get("/api/v1/authors/")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data


@pytest.mark.asyncio
async def test_get_authors_with_pagination(client: AsyncClient):
    response = await client.get("/api/v1/authors/?page=1&size=5")
    
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 5
    assert len(data["items"]) <= 5


@pytest.mark.asyncio
async def test_get_authors_with_filter(client: AsyncClient):
    response = await client.get("/api/v1/authors/?name=test&nationality=USA")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_get_author_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/v1/authors/99999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_author_unauthorized(client: AsyncClient):
    author_data = {
        "name": "Test Author",
        "biography": "Test biography",
        "birth_year": 1980,
        "nationality": "USA",
    }
    
    response = await client.post("/api/v1/authors/", json=author_data)
    assert response.status_code == 403