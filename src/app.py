from fastapi import FastAPI

from src.database import create_db_and_tables
from src.users import router as users_router
from src.auth.auth import router as auth_router


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get('/heartbeat')
async def heartbeat():
    return {'status': 'ok'}


app.include_router(users_router)
app.include_router(auth_router)
