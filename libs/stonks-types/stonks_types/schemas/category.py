from pydantic import BaseModel, Field
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str = Field(..., example="Electronics")
    parent_id: Optional[int] = Field(None, example=123)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int = Field(..., example=1)


    class Config:
        orm_mode = True


class CategoryResponse(Category):
    children: List[Category] = Field(...)
