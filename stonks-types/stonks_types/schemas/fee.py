from decimal import Decimal

from pydantic import BaseModel, Field


class FeeBase(BaseModel):
    stonks_id: int
    title: str = Field(..., example="Przewalutowanie")
    amount: Decimal = Field(..., example=10.5)
    currency: str = Field(..., example="PLN")


class FeeCreate(FeeBase):
    pass


class Fee(FeeBase):
    id: int

    class Config:
        orm_mode = True
