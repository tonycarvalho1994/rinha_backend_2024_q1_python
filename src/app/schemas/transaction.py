from datetime import datetime

from pydantic import BaseModel, Field, AliasChoices
from src.app.utils.enum import TransactionType


class Transaction(BaseModel):
    value: int = Field(alias="valor", validation_alias=AliasChoices("value", "valor"))
    type: TransactionType = Field(alias="tipo", validation_alias=AliasChoices("type", "tipo"))
    description: str = Field(alias="descricao", validation_alias=AliasChoices("description", "descricao"))
    carried_out: datetime = Field(alias="realizada_em", validation_alias=AliasChoices("carried_out", "realizada_em"), default_factory=datetime.now)

    @classmethod
    def create(cls, value: int, tx_type: TransactionType, description: str) -> "Transaction":
        return Transaction(
            value=value,
            type=tx_type,
            description=description.strip()
        )
