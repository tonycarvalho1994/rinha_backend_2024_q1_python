from pydantic import BaseModel, Field, AliasChoices
from src.app.schemas.transaction import Transaction


class Balance(BaseModel):
    total: int = Field(alias="total", validation_alias=AliasChoices("total", "total"))
    extract_date: str = Field(alias="data_extrato", validation_alias=AliasChoices("data_extrato", "extract_date"))
    limit: int = Field(alias="limite", validation_alias=AliasChoices("limite", "limit"))


class FindHistoryByIdOutput(BaseModel):
    balance: Balance = Field(alias="saldo", validation_alias=AliasChoices("balance", "saldo"))
    transactions: list[Transaction] = Field(alias="ultimas_transacoes", validation_alias=AliasChoices("transactions", "ultimas_transacoes"))
