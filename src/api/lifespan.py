import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.app.settings import DatabaseSettings
from src.infra.db import DatabasePSQL


@asynccontextmanager
async def lifespan(app: FastAPI):
    time.sleep(3)
    db_settings = DatabaseSettings()
    db = DatabasePSQL(db_settings)
    await db.setup()

    app.state.db = db

    yield
