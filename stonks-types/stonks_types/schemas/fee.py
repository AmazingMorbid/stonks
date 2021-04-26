from pydantic import BaseModel, Field


class FeeBase(BaseModel):
    title: str = Field(..., example="Przewalutowanie")
    amount: float = Field(..., example=10.5)
    currency: str = Field(..., example="PLN")


class FeeCreate(FeeBase):
    pass


class Fee(FeeBase):
    id: int

    class Config:
        orm_mode = True
