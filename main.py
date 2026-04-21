from fastapi import FastAPI, Depends
from api.router import router as books_router
from api.auth import router as auth_router
from api.rate_limiter import rate_limit_dependency

app = FastAPI(
    title="Library API",
    # ТИМЧАСОВО ВИМИКАЄМО ДЛЯ ЛАБИ 9:
    # dependencies=[Depends(rate_limit_dependency)] 
)

app.include_router(auth_router)
app.include_router(books_router)