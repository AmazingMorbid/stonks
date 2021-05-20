import logging
from datetime import datetime
from typing import List

import requests
from celery import group
from olx_sdk.models import Offer as OlxOffer
from olx_sdk.models import Status as OlxOfferStatus
from pydantic import parse_obj_as
from stonks_types.schemas import Offer, OfferUpdate, DeviceCreate

from celeryapp import app
from config import config, API_URL
from config.config import DEVICE_RECOGNIZER_API
from stonks_watcher.apis import olx
from stonks_watcher.exceptions import TaskFailed
from stonks_watcher.utils import older_than, newer_than

logger = logging.getLogger(__name__)


@app.task
def periodic_offers_update():
    """
    Update offers that:
        * are active
        * haven't been updated for more than 30 minutes (Default, config available)
    """
    params = {
        "is_active": True,
        "last_update_before": older_than(minutes=config["offers"]["update_older_than"])
    }

    try:
        r = requests.get(f"{API_URL}/v1/offers", params=params)
        r.raise_for_status()

        offers: List[Offer] = parse_obj_as(List[Offer], r.json())

        if (offers_count := len(offers)) == 0:
            logging.info("No offers to update.")
            return
        else:
            logger.info(f"Downloaded {offers_count} old offers.")

        group(update_offer.s(offer) for offer in offers)()

    except requests.exceptions.ConnectionError:
        raise TaskFailed("Could not connect to the device recognizer API")


@app.task
def update_offer(offer: Offer):
    logger.info(f"Updating offer id={offer.id}")
    olx_offer: OlxOffer = olx.offers.get_details(offer.id.split("-")[1])

    photos = [photo.link for photo in olx_offer.photos]
    offer_update: OfferUpdate = OfferUpdate(**olx_offer.dict(exclude={"photos", "category"}),
                                            photos=photos,
                                            category=offer.category,
                                            is_active=olx_offer.status == OlxOfferStatus.active,
                                            device_name=offer.device.name if offer.device is not None else None)
    try:
        r = requests.put(f"{API_URL}/v1/offers/{offer.id}", data=offer_update.json())
        r.raise_for_status()

        logger.info(f"Updated offer id={offer.id}")

        return offer
    except requests.exceptions.ConnectionError:
        raise TaskFailed("Could not connect to the device recognizer API")


@app.task
def periodic_get_device_info():
    params = {
        "is_active": True,
        "has_device": False,
        "limit": 500,
    }

    try:
        r = requests.get(f"{API_URL}/v1/offers", params=params)
        r.raise_for_status()

        offers: List[Offer] = parse_obj_as(List[Offer], r.json())
        offers_count = len(offers)

        if offers_count == 0:
            logging.info("No offers without device.")
            return
        else:
            logger.info(f"Downloaded {offers_count} offers without device.")

        texts = [offer.title for offer in offers]
        device_infos: List[dict] = requests.post(f"{DEVICE_RECOGNIZER_API}/get-info", json={"texts": texts}).json()["info"]

        group(create_device.s(offer, DeviceCreate(name=device_info["model"] or "_NO_DEVICE")) for offer, device_info in zip(offers, device_infos))()

    except requests.exceptions.ConnectionError:
        raise TaskFailed("Could not connect to the device recognizer API")


@app.task()
def create_device(offer: Offer, device: DeviceCreate):
    if device.name.lower() == "_no_device":
        logger.info(f"No device name was found in offer.")
        device_name = device.name

    else:
        logger.info(f"Creating device name={device.name}")

        device_name = None

        try:
            r = requests.post(f"{API_URL}/v1/devices", data=device.json())

            if r.status_code == 201:
                device_name = r.json()["name"]

            if r.status_code == 409:
                device_name = device.name

        except requests.ConnectionError:
            raise TaskFailed("Could not connect to the API")

    if device_name is None:
        return

    offer_update: OfferUpdate = OfferUpdate(**offer.dict(exclude={"device_name"}),
                                            device_name=device_name)

    try:
        r = requests.put(f"{API_URL}/v1/offers/{offer.id}", data=offer_update.json())
        r.raise_for_status()

        logger.info(f"Updated offer <id={offer.id}> with device_name={device_name}")

        return offer
    except requests.exceptions.ConnectionError:
        raise TaskFailed("Could not connect to the device recognizer API")
