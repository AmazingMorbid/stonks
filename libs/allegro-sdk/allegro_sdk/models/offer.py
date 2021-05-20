from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic.main import BaseModel


class Seller(BaseModel):
    id: str
    login: Optional[str] = None
    company: bool
    superSeller: bool


class Promotion(BaseModel):
    emphasized: bool
    bold: bool
    highlight: bool


class Price(BaseModel):
    amount: float
    currency: str


class Delivery(BaseModel):
    availableForFree: bool
    lowestPrice: Price


class Image(BaseModel):
    url: str


class SellingFormat(str, Enum):
    buy_now = "BUY_NOW"
    advertisement = "ADVERTISEMENT"
    auction = "AUCTION"


class SellingMode(BaseModel):
    format: SellingFormat
    popularity: Optional[int] = 0
    price: Price


class Stock(BaseModel):
    unit: str
    available: int


class Category(BaseModel):
    id: str


class Publication(BaseModel):
    endingAt: datetime


class Offer(BaseModel):
    id: str
    name: str
    seller: Seller
    promotion: Promotion
    delivery: Delivery
    images: List[Image]
    sellingMode: SellingMode
    stock: Stock
    category: Category
    publication: Optional[Publication] = None
