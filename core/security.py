from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from core.config import settings  # Беремо налаштування з config.py

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Для зручності експортуємо ключі, щоб api/deps.py не зламався
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(subject: Union[str, Any], expires_delta: timedelta, token_type: str) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(subject: Union[str, Any]) -> str:
    return create_token(subject, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), "access")

def create_refresh_token(subject: Union[str, Any]) -> str:
    return create_token(subject, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), "refresh")