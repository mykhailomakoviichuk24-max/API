import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from database.session import Base, get_db
from models.book import BookModel 
from main import app

DATABASE_URL = "postgresql+asyncpg://user:pass@db:5432/library_db"


engine_test = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_test = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
    await engine_test.dispose()

@pytest.fixture
async def db_session():
    
    async with async_session_test() as session:
        yield session

@pytest.fixture(autouse=True)
def override_get_db(db_session):
    
    app.dependency_overrides[get_db] = lambda: db_session

@pytest.fixture
async def client():
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac