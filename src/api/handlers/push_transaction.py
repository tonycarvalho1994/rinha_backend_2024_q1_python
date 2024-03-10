import json
from http import HTTPStatus

from fastapi import APIRouter, Request, Response
from src.api.schemas import PushTransactionInput
from src.app.schemas.transaction import Transaction
from src.app.utils.exceptions import CustomerNotFoundError, LimitExceededError
from src.infra.db import DatabasePSQL

push_transaction_router = APIRouter()


@push_transaction_router.post("/clientes/{customer_id}/transacoes")
async def push_transaction(
        customer_id: str,
        input_data: PushTransactionInput,
        request: Request,
):
    db: DatabasePSQL = request.app.state.db

    new_transaction = Transaction.create(
        value=input_data.value,
        description=input_data.description,
        tx_type=input_data.type
    )
    try:
        balance, limit = await db.push_transaction(customer_id, new_transaction)
        output = {"saldo": balance, "limite": limit}
        return output
    except CustomerNotFoundError:
        return Response(
            content='{"message": "consumer not found"}',
            headers={"content-type": "application/json"},
            status_code=HTTPStatus.NOT_FOUND,
        )
    except LimitExceededError:
        return Response(
            content='{"message": "limit exceeded"}',
            headers={"content-type": "application/json"},
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    except Exception:
        return Response(
            content='{"message": "bad request"}',
            headers={"content-type": "application/json"},
            status_code=HTTPStatus.BAD_REQUEST,
        )
