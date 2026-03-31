import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from database.session import Base, get_db
from main import app

DATABASE_URL = "postgresql+asyncpg://user:pass@db:5432/library_db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine_test():
    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session", autouse=True)
async def setup_db(engine_test):
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest.fixture
async def db_session(engine_test):
    factory = async_sessionmaker(engine_test, class_=AsyncSession)
    async with factory() as session: yield session

@pytest.fixture(autouse=True)
def override_db(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac