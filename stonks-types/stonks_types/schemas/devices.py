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
    __root__: List[PriceCreate]


class Price(PriceBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, example="pixel 3a")


class DeviceCreate(DeviceBase):
    price: Optional[List[PriceCreate]] = None


class DeviceUpdate(DeviceBase):
    price: Optional[List[PriceCreate]] = None


class Device(DeviceBase):
    price: List[Price]
    last_price_update: Optional[datetime] = None

    class Config:
        orm_mode = True
