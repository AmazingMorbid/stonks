from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Union, Optional

from pydantic import BaseModel


class OfferPromotion(BaseModel):
    highlighted: bool
    urgent: bool
    top_ad: bool
    options: List[str]
    b2c_ad_page: bool
    premium_ad_page: bool


class OfferParam(BaseModel):
    key: str
    name: str
    type: str
    value: Dict[str, Any]


class User(BaseModel):
    id: int
    other_ads_enabled: bool
    name: str
    logo: Any
    logo_ad_page: str
    social_network_account_type: str
    photo: str
    banner_mobile: str
    banner_desktop: str
    company_name: str
    about: str
    b2c_business_page: bool
    is_online: bool
    last_seen: datetime


class Contact(BaseModel):
    name: str
    phone: bool
    chat: bool
    negotiation: bool
    courier: bool


class Map(BaseModel):
    zoom: int
    lat: float
    lon: float
    radius: int
    show_detailed: bool


class City(BaseModel):
    id: int
    name: str
    normalized_name: str


class Region(BaseModel):
    id: int
    name: str
    normalized_name: str


class Location(BaseModel):
    city: City
    region: Region


class Photo(BaseModel):
    id: int
    filename: str
    rotation: int
    width: int
    height: int
    link: str


class Category(BaseModel):
    id: int
    type: str


class Delivery(BaseModel):
    offer_id: Optional[str]
    active: bool
    mode: str


class Safedeal(BaseModel):
    weight: int
    weight_grams: int
    status: str
    safedeal_blocked: bool


class Status(str, Enum):
    active = "active"
    disabled = "disabled"
    removed_by_user = "removed_by_user"
    moderated = "moderated"


class Offer(BaseModel):
    id: int
    url: str
    title: str
    description: str
    price: float
    currency: str
    price_negotiable: bool
    # promotion: OfferPromotion
    params: List[OfferParam]
    # key_params: List
    # business: bool
    # user: User
    status: Status
    # contact: Contact
    # map: Map
    # location: Location
    photos: List[Photo]
    # partner: Any
    # category: Category
    delivery: Delivery
    # safedeal: Safedeal
    # shop: Dict[str, str]
    # offer_type: str
    last_refresh_time: datetime
    created_time: datetime
