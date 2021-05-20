from fastapi import APIRouter

from stonks_api.api.v1.endpoints import offers, devices, stonks, prices, categories

api_router = APIRouter()
api_router.include_router(offers.router, prefix="/offers", tags=["Offers"])
api_router.include_router(devices.router, prefix="/devices", tags=["Devices"])
api_router.include_router(prices.router, prefix="/prices", tags=["Prices"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(stonks.router, tags=["Stonks"])
# api_router.include_router(device_recognizer.router, tags=["Device recognizer"])
