import json
from http import HTTPStatus

from fastapi import APIRouter, Request, Response
from src.app.utils.exceptions import CustomerNotFoundError
from src.infra.db import DatabasePSQL

get_history_router = APIRouter()


@get_history_router.get("/clientes/{customer_id}/extrato")
async def get_history_by_id(
        customer_id: str,
        request: Request,
):
    db: DatabasePSQL = request.app.state.db

    try:
        result = await db.find_history_by_customer_id(customer_id)
        output = result.model_dump(mode="json", by_alias=True)
        return result
    except CustomerNotFoundError:
        return Response(
            content='{"message": "consumer not found"}',
            headers={"content-type": "application/json"},
            status_code=HTTPStatus.NOT_FOUND,
        )
    except Exception:
        return Response(
            content='{"message": "bad request"}',
            headers={"content-type": "application/json"},
            status_code=HTTPStatus.BAD_REQUEST,
        )

