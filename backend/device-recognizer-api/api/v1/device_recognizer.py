from typing import List

from fastapi import APIRouter, Body, HTTPException

from device_recognizer import DeviceRecognizer
from schemas import DeviceInfo, DeviceInfoRequest, DeviceInfoResponse

router = APIRouter()
device_recognizer = DeviceRecognizer()


@router.get("/")
def index():
    return {
        "detail": "I'm alive"
    }


@router.post("/get-info", response_model=DeviceInfoResponse)
def get_device_info(texts: DeviceInfoRequest):
    if len(texts.texts) > 500:
        raise HTTPException(status_code=422, detail="You cannot process more than 500 texts at a time.")

    return DeviceInfoResponse(info=list(device_recognizer.get_info(texts.texts)))
