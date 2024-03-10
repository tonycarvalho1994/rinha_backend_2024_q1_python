from fastapi import FastAPI
from src.api.handlers.get_history import get_history_router
from src.api.handlers.push_transaction import push_transaction_router
from src.api.lifespan import lifespan


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)
    _app.include_router(get_history_router)
    _app.include_router(push_transaction_router)

    return _app


app = create_app()
