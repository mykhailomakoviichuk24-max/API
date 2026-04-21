import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import timedelta


from main import app
from core.security import create_token

client = TestClient(app)



@patch("api.rate_limiter.redis_client.incr", new_callable=AsyncMock)
@patch("api.rate_limiter.redis_client.expire", new_callable=AsyncMock)
def test_anonymous_user_under_limit(mock_expire, mock_incr):
    """Тест 1: Анонім ще не досяг ліміту"""
    mock_incr.return_value = 1 

    
    response = client.get("/books/") 
    
   
    assert response.status_code != 429 
    mock_incr.assert_called_once()
    mock_expire.assert_called_once_with("rate_limit:anon:testclient", 60)

@patch("api.rate_limiter.redis_client.incr", new_callable=AsyncMock)
def test_anonymous_user_over_limit(mock_incr):
    """Тест 2: Анонім перевищив ліміт"""
    mock_incr.return_value = 3 

    
    response = client.get("/books/")
    
    
    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded. Try again later."



def get_auth_headers(username="testuser"):
    """Допоміжна функція для генерації валідного токена для тестів"""
    token = create_token(username, timedelta(minutes=15), "access")
    return {"Authorization": f"Bearer {token}"}

@patch("api.rate_limiter.redis_client.incr", new_callable=AsyncMock)
@patch("api.rate_limiter.redis_client.expire", new_callable=AsyncMock)
def test_authorized_user_under_limit(mock_expire, mock_incr):
    """Тест 3: Авторизований юзер ще не досяг ліміту"""
    mock_incr.return_value = 5 # Уявімо, що це 5-й запит (ліміт 10)
    headers = get_auth_headers("johndoe")

    response = client.get("/books/", headers=headers)
    
    
    assert response.status_code != 429 
    mock_incr.assert_called_once_with("rate_limit:user:johndoe")

@patch("api.rate_limiter.redis_client.incr", new_callable=AsyncMock)
def test_authorized_user_over_limit(mock_incr):
    """Тест 4: Авторизований юзер перевищив ліміт у 10 запитів"""
    mock_incr.return_value = 11 
    headers = get_auth_headers("johndoe")

    response = client.get("/books/", headers=headers)
    
    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded. Try again later."