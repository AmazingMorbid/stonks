from fastapi import APIRouter

from device_recognizer import DeviceRecognizer
from schemas import DeviceInfo

router = APIRouter()
device_recognizer = DeviceRecognizer()


@router.get("/get-info", response_model=DeviceInfo)
def get_device_info(text: str):
    return device_recognizer.get_info(text)
