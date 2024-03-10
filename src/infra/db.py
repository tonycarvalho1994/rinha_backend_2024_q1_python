from datetime import datetime

import asyncpg
from asyncpg.pool import Pool
from src.app.schemas.transaction import Transaction
from src.app.settings import DatabaseSettings
from src.app.utils.enum import TransactionType
from src.app.utils.exceptions import CustomerNotFoundError, LimitExceededError
from src.infra.queries import SELECT_BALANCE_LIMIT_QUERY, GET_HISTORY_LIMIT_10_QUERY, INSERT_TRANSACTION_QUERY, \
    UPDATE_BALANCE_QUERY
from src.infra.schemas import FindHistoryByIdOutput, Balance


class DatabasePSQL:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self._pool: Pool | None = None

    async def setup(self):
        conn_str = (
            "postgres://{user}:{password}@{host}:{port}/{db}".format(
                user=self._settings.DB_USER,
                password=self._settings.DB_PASS,
                host=self._settings.DB_HOST,
                port=self._settings.DB_PORT,
                db=self._settings.DB_NAME
            )
        )
        self._pool = await asyncpg.create_pool(
            dsn=conn_str,
            min_size=self._settings.DB_MAX_CONNECTIONS - 1,
            max_size=self._settings.DB_MAX_CONNECTIONS,
        )

    async def find_history_by_customer_id(self, customer_id: str) -> FindHistoryByIdOutput:
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                customer = await conn.fetchrow(SELECT_BALANCE_LIMIT_QUERY, customer_id)
                if customer is None:
                    raise CustomerNotFoundError()

                limit = customer["limite"]
                current_balance = customer["saldo"]

                tx_results = await conn.fetch(GET_HISTORY_LIMIT_10_QUERY, customer_id)
                transactions = []
                for tx in tx_results:
                    transactions.append(
                        Transaction(
                            value=tx["valor"],
                            type=tx["tipo"],
                            description=tx["descricao"].strip(),
                            carried_out=tx["realizada_em"],
                        )
                    )

                return FindHistoryByIdOutput(
                    balance=Balance(
                        total=current_balance,
                        extract_date=datetime.now().isoformat(),
                        limit=limit,
                    ),
                    transactions=transactions
                )

    async def push_transaction(self, customer_id: str, transaction: Transaction) -> tuple[int, int]:
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                customer = await conn.fetchrow(SELECT_BALANCE_LIMIT_QUERY, customer_id)
                if customer is None:
                    raise CustomerNotFoundError()

                limit = customer["limite"]
                current_balance = customer["saldo"]
                new_balance = 0

                if transaction.type == TransactionType.DEBIT:
                    new_balance = current_balance - transaction.value
                elif transaction.type == TransactionType.CREDIT:
                    new_balance = current_balance + transaction.value

                if any([new_balance < limit * -1, new_balance > limit]):
                    raise LimitExceededError()

                await conn.execute(
                    INSERT_TRANSACTION_QUERY,
                    customer_id,
                    transaction.value,
                    transaction.type.value,
                    transaction.description,
                    transaction.carried_out,
                )
                await conn.execute(
                    UPDATE_BALANCE_QUERY,
                    new_balance,
                    customer_id
                )

                return new_balance, limit
