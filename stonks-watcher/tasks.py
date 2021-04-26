import logging
from datetime import datetime, timedelta
from typing import List

import pytz
import requests
from celery import Celery, group
from pydantic import parse_obj_as

from stonks_types.schemas import Offer, OfferUpdate
from olx_sdk.models import Offer as OlxOffer
from olx_sdk.models import Status as OlxOfferStatus

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from config import API_URL, olx, OFFER_UPDATE_INTERVAL, OFFER_UPDATE_OLDER_THAN, allegro

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
    sender.add_periodic_task(OFFER_UPDATE_INTERVAL,
                             update_offers.s(),
                             name="Every minute check for offers older than 30 minutes and update them")


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
    older_than_datetime = (datetime.now(pytz.utc) - timedelta(minutes=OFFER_UPDATE_OLDER_THAN)).isoformat()

    try:
        r = requests.get(f"{API_URL}/v1/offers", params={"older_than": older_than_datetime})
        logging.info("Downloaded old offers.")
        offers: List[Offer] = parse_obj_as(List[Offer], r.json())

        return group(update_offer.s(offer) for offer in offers)()

    except requests.exceptions.ConnectionError as e:
        logging.error("Could not connect to the API")
