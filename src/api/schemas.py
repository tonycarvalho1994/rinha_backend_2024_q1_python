from pydantic import BaseModel, Field, AliasChoices
from src.app.utils.enum import TransactionType


class PushTransactionInput(BaseModel):
    value: int = Field(alias="valor", validation_alias=AliasChoices("value", "valor"))
    type: TransactionType = Field(alias="tipo", validation_alias=AliasChoices("type", "tipo"))
    description: str = Field(
        alias="descricao",
        validation_alias=AliasChoices("description", "descricao"),
        max_length=10,
        min_length=1,
    )
