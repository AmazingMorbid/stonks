# from fastapi import APIRouter
#
# from stonks_api.device_recognizer import DeviceRecognizer, DeviceInfo
#
# device_recognizer = DeviceRecognizer()
#
# router = APIRouter()
#
#
# @router.get("/device-recognizer", response_model=DeviceInfo)
# def get_device_info(text: str):
#     return device_recognizer.get_info(text)
