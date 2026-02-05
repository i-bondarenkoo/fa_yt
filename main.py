from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.models.base import Base
from core.models.db_helper import db_helper, DatabaseHelper
import uvicorn
from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1
from core.config import settings


# запустить создание новой БД и таблиц при запуске
# функция генератор
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # создание новой БД
#     async with db_helper.engine.begin() as connection:
#         await connection.run_sync(Base.metadata.create_all)
#     yield


# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(
    router_v1,
    prefix=settings.api_v1_prefix,
)
app.include_router(items_router)
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello, index",
    }


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


@app.get("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "sum": a + b,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
