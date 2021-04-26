from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field

from stonks_types.schemas import DeliveryCreate, Delivery


class OfferBase(BaseModel):
    url: str = Field(..., example="https://example.org")
    title: str = Field(..., example="Telefon pixel 3a")
    description: Optional[str] = Field(None, example="Sprzedam telefon pixel 3a")
    category: str = Field(..., example="smartphone")
    price: float = Field(..., example=500.59)
    currency: str = Field(..., example="PLN")
    photos: List[str] = Field([])
    is_active: bool
    last_refresh_time: Optional[datetime] = Field(None, example=datetime.now())
    last_scraped_time: datetime = Field(..., example=datetime.now())


class OfferCreate(OfferBase):
    id: str
    deliveries: Optional[List[DeliveryCreate]] = None


class OfferUpdate(OfferBase):
    pass


class Offer(OfferBase):
    id: str
    deliveries: List[Delivery] = []

    class Config:
        orm_mode = True
