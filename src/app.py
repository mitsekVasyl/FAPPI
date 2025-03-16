from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import create_db_and_tables
from src.exceptions import UniqueConstraintError, unique_constraint_handler
from src.users import router as users_router
from src.auth.auth import router as auth_router


@asynccontextmanager
async def on_startup(a: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=on_startup)


@app.get('/heartbeat')
async def heartbeat():
    return {'status': 'ok'}


app.include_router(users_router)
app.include_router(auth_router)


app.add_exception_handler(UniqueConstraintError, unique_constraint_handler)
