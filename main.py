from fastapi import FastAPI
from api.router import router

app = FastAPI(
    title="Library Management API",
    description="API для керування бібліотекою книг",
    version="1.0.0"
)


app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Вітаємо у Library API! Перейдіть на /docs для документації."}