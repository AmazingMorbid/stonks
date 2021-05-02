import logging
from datetime import datetime, timedelta
from typing import List

import pytz
import requests
from celery import Celery, group
from pydantic import parse_obj_as

from stonks_types.schemas import Offer, OfferUpdate, Device
from olx_sdk.models import Offer as OlxOffer
from olx_sdk.models import Status as OlxOfferStatus

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from config import olx, allegro, config, API_URL
from stonks_watcher.utils import older_than_datetime_iso

sentry_sdk.init(
    dsn='https://f1e132df10f04ba398e0750959149471@o577912.ingest.sentry.io/5733971',
    integrations=[CeleryIntegration()],
    sample_rate=0.2,
)

app = Celery("tasks", backend="rpc://localhost/", broker="pyamqp://localhost/")
app.conf.timezone = "Europe/Warsaw"


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]


app.config_from_object(CeleryConfig)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(config["offers"]["update_interval"],
                             update_offers.s(),
                             name="Update offers")
    sender.add_periodic_task(config["prices"]["update_interval"],
                             update_device_prices.s(),
                             name="Update prices.")


@app.task
def find_stonks(offer: Offer):
    allegro_offers = allegro.offers.listing(**{"category.id": 165,
                                               "phrase": offer.title,
                                               "include": ["-all", "items"],
                                               "sellingMode.format": "BUY_NOW",
                                               "limit": 60,
                                               "sort": "+price",
                                               "offset": 0,
                                               "parameter.11323": "11323_2"})
    allegro_offers = allegro_offers[:10]

    if allegro_offers > 0:
        for allegro_offer in allegro_offers:
            print(allegro_offer.sellingMode)


@app.task
def update_offer(offer: Offer):
    logging.info(f"Updating offer id={offer.id}")
    olx_offer: OlxOffer = olx.offers.get_details(offer.id.split("-")[1])

    photos = [photo.link for photo in olx_offer.photos]
    offer_update: OfferUpdate = OfferUpdate(**olx_offer.dict(exclude={"photos": ...}),
                                            photos=photos,
                                            last_scraped_time=datetime.now(pytz.utc),
                                            category=offer.category,
                                            is_active=olx_offer.status == OlxOfferStatus.active)
    r = requests.put(f"{API_URL}/v1/offers/{offer.id}", data=offer_update.json())
    r.raise_for_status()
    offer = Offer(**r.json())
    logging.info(f"Updated offer id={offer.id}")
    return offer


@app.task
def update_offers():
    older_than = older_than_datetime_iso(timedelta(minutes=config["offers"]["update_older_than"]))

    try:
        r = requests.get(f"{API_URL}/v1/offers", params={"older_than": older_than})
        logging.info("Downloaded old offers.")
        offers: List[Offer] = parse_obj_as(List[Offer], r.json())

        return group(update_offer.s(offer) for offer in offers)()

    except requests.exceptions.ConnectionError as e:
        logging.error("Could not connect to the API")


@app.task
def update_device_prices():
    params = {"older_than": older_than_datetime_iso(timedelta(days=config["prices"]["update_older_than"])),
              "limit": config["prices"]["update_count"]}

    try:
        r = requests.get(f"{API_URL}/v1/devices", params=params)
        logging.info("Downloaded old devices.")
        devices: List[Device] = parse_obj_as(List[Device], r.json())

    except requests.exceptions.ConnectionError as e:
        logging.error("Could not connect to the API")
