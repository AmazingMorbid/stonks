import logging
from datetime import timedelta
from typing import List

import requests
from celery import group
from pydantic import parse_obj_as
from stonks_types.schemas import Device, PricesCreate, PriceCreate

from celeryapp import app
from config import allegro, config, API_URL
from stonks_watcher.utils import older_than_datetime_iso


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

    try:
        r = requests.get(f"{API_URL}/v1/devices", params=params)
        r.raise_for_status()

        devices: List[Device] = parse_obj_as(List[Device], r.json())

        if len(devices) == 0:
            logging.info("No devices to update.")
            return
        else:
            logging.info(f"Downloaded {len(devices)} old devices.")

        group((get_allegro_prices.s(device) |
               update_device_prices.s(device))
              for device in devices)()
    except requests.exceptions.ConnectionError as e:
        logging.error("Could not connect to the API")


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
    try:
        if len(prices) == 0:
            logging.warning(f"No prices for {device.name} were found on allegro. Creating [] prices to update last_price_update.")
            r = requests.post(f"{API_URL}/v1/devices/{device.name}/prices", json=[])
            r.raise_for_status()
            return r.json()

        prices_create = PricesCreate(__root__=prices)
        r = requests.post(f"{API_URL}/v1/devices/{device.name}/prices",
                          data=prices_create.json())
        r.raise_for_status()

        return r.json()
    except requests.exceptions.ConnectionError as e:
        logging.error("Could not connect to the API")
