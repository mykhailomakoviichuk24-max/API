import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_and_delete_book():
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        
        new_book_data = {
            "title": "Майстер і Маргарита",
            "author": "Михайло Булгаков",
            "release_year": 1967,
            "status": "наявна"
        }
        response = await ac.post("/books/", json=new_book_data)
        assert response.status_code == 201
        book_id = response.json()["id"]

        
        get_res = await ac.get(f"/books/{book_id}")
        assert get_res.status_code == 200
        assert get_res.json()["title"] == "Майстер і Маргарита"

        
        del_res = await ac.delete(f"/books/{book_id}")
        assert del_res.status_code == 204

        
        del_res_again = await ac.delete(f"/books/{book_id}")
        assert del_res_again.status_code == 204

@pytest.mark.asyncio
async def test_validation_error():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        
        bad_data = {"title": "Test", "author": "Author", "release_year": -1}
        response = await ac.post("/books/", json=bad_data)
        assert response.status_code == 422 