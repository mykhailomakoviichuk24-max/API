from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from core.redis import redis_client
from core.config import settings

async def get_user_identifier(request: Request) -> tuple[str, int]:
    """
    Визначає, хто робить запит, і повертає ключ для Redis та ліміт.
    """
    auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if username:
                return f"rate_limit:user:{username}", 10  # 10 запитів для авторизованих
        except JWTError:
            pass 

    client_ip = request.client.host if request.client else "127.0.0.1"
    return f"rate_limit:anon:{client_ip}", 2  # 2 запити для анонімів

async def rate_limit_dependency(request: Request):
    """
    Залежність (Dependency), яка перевіряє ліміти перед виконанням запиту.
    """
    redis_key, limit = await get_user_identifier(request)

    current_requests = await redis_client.incr(redis_key)

    if current_requests == 1:
        await redis_client.expire(redis_key, 60)

    if current_requests > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )