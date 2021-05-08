import logging
from datetime import datetime, timedelta
from typing import List

import requests
from celery import group
from olx_sdk.models import Offer as OlxOffer
from olx_sdk.models import Status as OlxOfferStatus
from pydantic import parse_obj_as
from stonks_types.schemas import Offer, OfferUpdate

from celeryapp import app
from config import config, API_URL
from stonks_watcher.apis import olx
from stonks_watcher.utils import older_than


@app.task
def periodic_offers_update():
    params = {
        "older_than": older_than(timedelta(minutes=config["offers"]["update_older_than"]))
    }

    try:
        r = requests.get(f"{API_URL}/v1/offers", params=params)
        r.raise_for_status()

        offers: List[Offer] = parse_obj_as(List[Offer], r.json())

        if (offers_count := len(offers)) == 0:
            logging.info("No offers to update.")
            return
        else:
            logging.info(f"Downloaded {offers_count} old offers.")

        group(update_offer.s(offer) for offer in offers)()

    except requests.exceptions.ConnectionError as e:
        logging.error("Could not connect to the API")


@app.task
def update_offer(offer: Offer):
    logging.info(f"Updating offer id={offer.id}")
    olx_offer: OlxOffer = olx.offers.get_details(offer.id.split("-")[1])

    photos = [photo.link for photo in olx_offer.photos]
    offer_update: OfferUpdate = OfferUpdate(**olx_offer.dict(exclude={"photos": ...}),
                                            photos=photos,
                                            last_scraped_time=datetime.utcnow(),
                                            category=offer.category,
                                            is_active=olx_offer.status == OlxOfferStatus.active,
                                            device_name=offer.device.name if offer.device is not None else None)
    try:
        r = requests.put(f"{API_URL}/v1/offers/{offer.id}", data=offer_update.json())
        r.raise_for_status()

        logging.info(f"Updated offer id={offer.id}")

        return offer
    except requests.exceptions.ConnectionError as e:
        logging.error("Could not connect to the API")
