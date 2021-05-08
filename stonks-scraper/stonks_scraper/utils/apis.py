import logging
import os
from typing import Optional

import requests
import sentry_sdk
from stonks_types.schemas import DeviceCreate


DEVICE_RECOGNIZER_API = os.getenv("DEVICE_RECOGNIZER_API_URL", "http://device-recognizer-api")
STONKS_API = os.getenv("STONKS_API_URL", "http://stonks-api")


def get_device_model(text: str) -> Optional[str]:
    # Get device info from device recognizer
    device_info = get_device_info(text)

    if device_info is None:
        return

    # Get device model and post it to the db
    device_model = device_info["model"]
    if device_model is None or len(device_model) < 3:
        logging.debug(f"No device was extracted from string {text}")
        return

    device_model = create_device(DeviceCreate(name=device_model))

    return device_model


def get_device_info(text: str) -> Optional[dict]:
    try:
        r = requests.get(f"{DEVICE_RECOGNIZER_API}/api/v1/get-info", params={"text": text})
        print("get_device_info status:", r.status_code)
        r.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        sentry_sdk.capture_exception(errh)
        logging.exception("Http Error")

    except requests.exceptions.ConnectionError as errc:
        sentry_sdk.capture_exception(errc)
        logging.exception("Error Connecting")

    except requests.exceptions.Timeout as errt:
        sentry_sdk.capture_exception(errt)
        logging.exception("Timeout Error")

    except requests.exceptions.RequestException as err:
        sentry_sdk.capture_exception(err)
        logging.exception("OOps: Something Else")

    else:
        return r.json()


def create_device(device: DeviceCreate) -> Optional[str]:
    try:
        print(device)
        r = requests.post(f"{STONKS_API}/v1/devices", data=device.json())
        print("create_device status:", r.status_code)
        if r.status_code != 409:
            r.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        sentry_sdk.capture_exception(errh)
        logging.exception("Http Error")

    except requests.exceptions.ConnectionError as errc:
        sentry_sdk.capture_exception(errc)
        logging.exception("Error Connecting")

    except requests.exceptions.Timeout as errt:
        sentry_sdk.capture_exception(errt)
        logging.exception("Timeout Error")

    except requests.exceptions.RequestException as err:
        sentry_sdk.capture_exception(err)
        logging.exception("OOps: Something Else")

    else:
        return device.name.lower()
