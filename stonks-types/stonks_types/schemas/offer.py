from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from stonks_types.schemas import DeliveryCreate, Delivery, DeviceCreate, Device


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
    device: Optional[str] = None


class OfferUpdate(OfferBase):
    device: Optional[str] = None
    last_stonks_check: Optional[datetime] = None


class Offer(OfferBase):
    id: str
    deliveries: List[Delivery] = []
    device: Device = None
    last_stonks_check: Optional[datetime] = None

    class Config:
        orm_mode = True
