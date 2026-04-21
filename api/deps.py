from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.security import SECRET_KEY, ALGORITHM  # Імпорт з твоєї папки core

# Вказуємо шлях, де лежить логін, щоб Swagger знав, куди надсилати дані
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Функція-залежність для перевірки Access Token.
    Якщо токен валідний — повертає ім'я користувача.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодуємо токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        # Перевіряємо, чи це саме Access токен, а не Refresh
        if username is None or token_type != "access":
            raise credentials_exception
            
        return username
    except JWTError:
        raise credentials_exception