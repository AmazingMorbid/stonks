from fastapi import APIRouter

from api.v1 import device_recognizer

api_router = APIRouter()
api_router.include_router(router=device_recognizer.router)
