from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from stonks_types.schemas import Offer, Fee, FeeCreate


class StonksBase(BaseModel):
    low_price: float = Field(...)
    high_price: float = Field(...)
    average_price: float = Field(...)
    median_price: float = Field(...)
    harmonic_price: float = Field(...)


class StonksCreate(StonksBase):
    fees: List[FeeCreate]
    created_at: datetime = datetime.utcnow()


class Stonks(StonksBase):
    id: int
    offer: Offer
    fees: List[Fee]
    created_at: datetime

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
    harmonic_price_asc = "harmonic_price_asc"
    harmonic_price_desc = "harmonic_price_desc"
