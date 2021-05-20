from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class DeliveryBase(BaseModel):
    title: Optional[str] = Field(None, example="Paczkomat")
    price: float = Field(..., example=8.99)
    currency: str = Field(..., example="PLN")


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(DeliveryBase):
    pass


class Delivery(DeliveryBase):
    id: int

    class Config:
        orm_mode = True
