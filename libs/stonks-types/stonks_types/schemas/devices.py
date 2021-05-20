from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PriceBase(BaseModel):
    source: str = Field(..., example="allegro")
    price: float = Field(..., example="69")
    currency: str = Field(..., min_length=3, max_length=3, example="PLN")


class PriceCreate(PriceBase):
    date: datetime = datetime.utcnow()


class PricesCreate(BaseModel):
    prices: List[PriceCreate]


class Price(PriceBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, example="pixel 3a")
    category: Optional[str] = Field(None, min_length=3, example="smartphones/google")

class DeviceCreate(DeviceBase):
    # price: Optional[List[PriceCreate]] = None
    pass


class DeviceUpdate(DeviceBase):
    # price: Optional[List[PriceCreate]] = None
    pass


class Device(DeviceBase):
    last_price_update: Optional[datetime] = None

    class Config:
        orm_mode = True


class Prices(BaseModel):
    prices: List[Price]
