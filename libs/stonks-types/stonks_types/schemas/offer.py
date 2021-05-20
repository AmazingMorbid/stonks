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
    last_stonks_check: Optional[datetime] = None


class OfferCreate(OfferBase):
    id: str
    deliveries: Optional[List[DeliveryCreate]] = None
    device_name: Optional[str] = None
    scraped_at: datetime = Field(..., example=datetime.now())


class OfferUpdate(OfferBase):
    device_name: Optional[str] = None


class Offer(OfferBase):
    id: str
    deliveries: List[Delivery] = []
    device: Device = None
    scraped_at: datetime = Field(..., example=datetime.now())
    last_update_at: Optional[datetime] = Field(None, example=datetime.now())

    class Config:
        orm_mode = True
