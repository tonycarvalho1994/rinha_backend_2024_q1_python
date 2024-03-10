from pydantic import BaseModel, Field


class Customer(BaseModel):
    id: str
    limit: int = Field(alias="limite")
    transactions: list
