from fastapi import FastAPI
from api.router import router as books_router # БЕЗ app.
from api.auth import router as auth_router   # БЕЗ app.

app = FastAPI(title="Library API (JWT)")

app.include_router(auth_router)
app.include_router(books_router)