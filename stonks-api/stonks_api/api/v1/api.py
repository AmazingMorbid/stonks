from fastapi import APIRouter

from stonks_api.api.v1.endpoints import offers
from stonks_api.api.v1.endpoints import stonks

api_router = APIRouter()
api_router.include_router(offers.router, prefix="/offers", tags=["Offers"])
api_router.include_router(stonks.router, tags=["Stonks"])
