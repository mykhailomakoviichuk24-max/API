import os

class Settings:
    PROJECT_NAME: str = "Library API"
    PROJECT_VERSION: str = "1.0.0"

    # Секретні ключі для JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_FOR_LIBRARY_PROJECT")
    ALGORITHM: str = "HS256"
    
    # Терміни дії токенів
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Налаштування бази даних
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongo:27017")
    DATABASE_NAME: str = "library_db"

# Створюємо екземпляр класу ПІСЛЯ самого класу
settings = Settings() 
# НІЯКИХ "from core.config import settings" ТУТ НЕ ТРЕБА!