import pytest
from uuid import UUID

@pytest.mark.asyncio
async def test_create_book(client):
    response = await client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "release_year": 2024,
        "status": "наявна"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"
    return response.json()["id"]

@pytest.mark.asyncio
async def test_get_books_pagination(client):
    
    for i in range(3):
        await client.post("/books/", json={
            "title": f"Book {i}",
            "author": "Author",
            "release_year": 2000 + i
        })
    
    
    response = await client.get("/books/?limit=2&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_delete_book_idempotent(client):
   
    res = await client.post("/books/", json={
        "title": "To Delete", "author": "A", "release_year": 2022
    })
    book_id = res.json()["id"]

   
    response1 = await client.delete(f"/books/{book_id}")
    assert response1.status_code == 204

    
    response2 = await client.delete(f"/books/{book_id}")
    assert response2.status_code == 204

@pytest.mark.asyncio
async def test_validation_error(client):
    
    response = await client.post("/books/", json={
        "title": "Bad", "author": "B", "release_year": -5
    })
    assert response.status_code == 422