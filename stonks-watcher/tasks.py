# @app.task
# def find_stonks(offer: Offer):
#     allegro_offers = allegro.offers.listing(**{"category.id": 165,
#                                                "phrase": offer.title,
#                                                "include": ["-all", "items"],
#                                                "sellingMode.format": "BUY_NOW",
#                                                "limit": 60,
#                                                "sort": "+price",
#                                                "offset": 0,
#                                                "parameter.11323": "11323_2"})
#     allegro_offers = allegro_offers[:10]
#
#     if allegro_offers > 0:
#         for allegro_offer in allegro_offers:
#             print(allegro_offer.sellingMode)
#
#
# @app.task
# def update_offer(offer: Offer):
#     logging.info(f"Updating offer id={offer.id}")
#     olx_offer: OlxOffer = olx.offers.get_details(offer.id.split("-")[1])
#
#     photos = [photo.link for photo in olx_offer.photos]
#     offer_update: OfferUpdate = OfferUpdate(**olx_offer.dict(exclude={"photos": ...}),
#                                             photos=photos,
#                                             last_scraped_time=datetime.now(pytz.utc),
#                                             category=offer.category,
#                                             is_active=olx_offer.status == OlxOfferStatus.active)
#     r = requests.put(f"{API_URL}/v1/offers/{offer.id}", data=offer_update.json())
#     r.raise_for_status()
#     offer = Offer(**r.json())
#     logging.info(f"Updated offer id={offer.id}")
#     return offer
#
#
# @app.task
# def update_offers():
#     older_than = older_than_datetime_iso(timedelta(minutes=config["offers"]["update_older_than"]))
#
#     try:
#         r = requests.get(f"{API_URL}/v1/offers", params={"older_than": older_than})
#         logging.info("Downloaded old offers.")
#         offers: List[Offer] = parse_obj_as(List[Offer], r.json())
#
#         return group(update_offer.s(offer) for offer in offers)()
#
#     except requests.exceptions.ConnectionError as e:
#         logging.error("Could not connect to the API")
#


import logging
from datetime import datetime, timedelta, time
from time import sleep
from typing import List

import requests
from celery import Celery, group, chain
from pydantic import parse_obj_as

from stonks_types.schemas import Offer, OfferUpdate, Device, PricesCreate, PriceCreate
from olx_sdk.models import Offer as OlxOffer
from olx_sdk.models import Status as OlxOfferStatus
from allegro_sdk.models import Offer as AllegroOffer

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from config import olx, allegro, config, API_URL
from stonks_watcher.utils import older_than_datetime_iso

sentry_sdk.init(
    dsn='https://f1e132df10f04ba398e0750959149471@o577912.ingest.sentry.io/5733971',
    integrations=[CeleryIntegration()],
    sample_rate=0.2,
)

app = Celery("tasks", broker="pyamqp://root:root@127.0.0.1:5672//")


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]


app.config_from_object(CeleryConfig)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(config["offers"]["update_interval"],
    #                          update_offers.s(),
    #                          name="Update offers")
    sender.add_periodic_task(config["prices"]["update_interval"] * 60,
                             periodic_prices_update.s(),
                             name="Periodic prices update.")


@app.task
def periodic_prices_update():
    """
    Get devices which prices haven't been refreshed for longer than `update_older_than`
    and for each device, get the latest prices from allegro and update them using `update_device_price`.
    """
    params = {
        "last_price_update_before": older_than_datetime_iso(timedelta(days=config["prices"]["update_older_than"])),
        "limit": config["prices"]["update_count"]
    }

    r = requests.get(f"{API_URL}/v1/devices", params=params)
    devices: List[Device] = parse_obj_as(List[Device], r.json())

    if len(devices) == 0:
        logging.info("No devices to update.")
        return
    else:
        logging.info(f"Downloaded {len(devices)} old devices.")

    group((get_allegro_prices.s(device) |
           update_device_prices.s(device))
          for device in devices)()


@app.task
def get_allegro_prices(device: Device) -> List[PriceCreate]:
    """
    Get prices of device from allegro.
    :param device: The device you are looking for a price for.
    :return: List of PriceCreate used in stonks-api.
    """
    allegro_offers = allegro.offers.listing(**{"category.id": 165,
                                               "phrase": device.name,
                                               "include": ["-all", "items"],
                                               "sellingMode.format": "BUY_NOW",
                                               "limit": 10,
                                               "sort": "+price",
                                               "offset": 0,
                                               "parameter.11323": "11323_2",
                                               "fallback": False})
    allegro_offers_count = len(allegro_offers)
    logging.info(f"Downloaded {allegro_offers_count} offers from allegro.")

    return [PriceCreate(source="allegro",
                        price=offer.sellingMode.price.amount,
                        currency=offer.sellingMode.price.currency) for offer in allegro_offers]


@app.task
def update_device_prices(prices: List[PriceCreate], device: Device):
    """
    Update prices of a device in stonks-database.
    :param prices: List of new prices.
    :param device: Device for which update is made.
    :return: Response from API.
    """
    if len(prices) == 0:
        logging.warning(f"No prices for {device.name} were found on allegro. Creating [] prices to update last_price_update.")
        r = requests.post(f"{API_URL}/v1/devices/{device.name}/prices", json=[])
        return r.json()

    prices_create = PricesCreate(__root__=prices)
    r = requests.post(f"{API_URL}/v1/devices/{device.name}/prices",
                      data=prices_create.json())
    return r.json()
