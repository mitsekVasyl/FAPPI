from fastapi import FastAPI

from src.database import create_db_and_tables
from src.users import router as users_router


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(users_router)
