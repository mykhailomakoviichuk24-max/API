import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_and_delete_book():
    # Використовуємо ASGITransport для тестування асинхронного додатку
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Створюємо книгу
        new_book_data = {
            "title": "Майстер і Маргарита",
            "author": "Михайло Булгаков",
            "release_year": 1967,
            "status": "наявна"
        }
        response = await ac.post("/books/", json=new_book_data)
        assert response.status_code == 201
        book_id = response.json()["id"]

        # 2. Перевіряємо, чи вона є в списку
        get_res = await ac.get(f"/books/{book_id}")
        assert get_res.status_code == 200
        assert get_res.json()["title"] == "Майстер і Маргарита"

        # 3. Видаляємо книгу
        del_res = await ac.delete(f"/books/{book_id}")
        assert del_res.status_code == 204

        # 4. Перевіряємо ідемпотентність (видаляємо ще раз)
        del_res_again = await ac.delete(f"/books/{book_id}")
        assert del_res_again.status_code == 204

@pytest.mark.asyncio
async def test_validation_error():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Спробуємо відправити невалідний рік (наприклад, -1)
        bad_data = {"title": "Test", "author": "Author", "release_year": -1}
        response = await ac.post("/books/", json=bad_data)
        assert response.status_code == 422 # Помилка валідації Pydantic