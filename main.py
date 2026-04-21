from fastapi import FastAPI, Depends
from api.router import router as books_router
from api.auth import router as auth_router
from api.rate_limiter import rate_limit_dependency # Наш лімітер

app = FastAPI(
    title="Library API",
    dependencies=[Depends(rate_limit_dependency)] # Застосовуємо до ВСІХ запитів
)

app.include_router(auth_router)
app.include_router(books_router)