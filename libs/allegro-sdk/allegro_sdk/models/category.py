from typing import Optional

from pydantic import BaseModel


class Options(BaseModel):
    variantsByColorPatternAllowed: bool
    advertisement: bool
    advertisementPriceOptional: bool
    offersWithProductPublicationEnabled: bool
    productCreationEnabled: bool
    customParametersEnabled: bool


class Parent(BaseModel):
    id: str


class Category(BaseModel):
    id: str
    leaf: bool
    name: str
    options: Options
    parent: Optional[Parent] = None
