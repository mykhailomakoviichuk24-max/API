from fastapi import FastAPI
from api.router import router

app = FastAPI(title="Library API (MongoDB + Limit-Offset)")

app.include_router(router)