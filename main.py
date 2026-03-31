from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.router import router
from database.session import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Library API - Cursor Pagination", lifespan=lifespan)
app.include_router(router)