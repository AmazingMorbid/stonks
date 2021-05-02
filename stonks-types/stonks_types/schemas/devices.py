from typing import List, Optional

from pydantic import BaseModel, Field


class PriceBase(BaseModel):
    source: str = Field(..., example="allegro")
    price: float = Field(..., example="69")
    currency: str = Field(..., min_length=3, max_length=3, example="PLN")


class PriceCreate(PriceBase):
    pass


class Price(PriceBase):
    id: int

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, example="pixel 3a")


class DeviceCreate(DeviceBase):
    price: Optional[List[PriceCreate]] = None


class Device(DeviceBase):
    price: List[Price]

    class Config:
        orm_mode = True
