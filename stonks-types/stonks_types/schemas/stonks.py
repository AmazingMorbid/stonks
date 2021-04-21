from decimal import Decimal
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from stonks_types.schemas import Offer, Fee


class StonksBase(BaseModel):
    offer: Offer

    fees: List[Fee]

    low_price: Decimal = Field(..., example=100.0)
    high_price: Decimal = Field(..., example=300.0)
    average_price: Decimal = Field(..., example=200)
    median_price: Decimal = Field(..., example=150)


class StonksCreate(StonksBase):
    pass


class Stonks(StonksBase):
    id: int

    class Config:
        orm_mode = True


class StonksSortBy(str, Enum):
    stonks_amount_asc = "stonks_amount_asc"
    stonks_amount_desc = "stonks_amount_desc"
    low_price_asc = "low_price_asc"
    low_price_desc = "low_price_desc"
    high_price_asc = "high_price_asc"
    high_price_desc = "high_price_desc"
    average_price_asc = "average_price_asc"
    average_price_desc = "average_price_desc"
    median_price_asc = "median_price_asc"
    median_price_desc = "median_price_desc"
