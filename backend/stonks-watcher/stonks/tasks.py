import logging
import statistics
from datetime import datetime
from pprint import pprint
from typing import List

import requests
from pydantic import parse_obj_as
from stonks_types.schemas import Offer, Price, Prices, StonksCreate, FeeCreate, OfferUpdate

from celeryapp import app
from config.config import API_URL, config
from stonks_watcher.utils import older_than, newer_than

logger = logging.getLogger(__name__)


fees = {
    "sell": {
        "smartphones/samsung": 0.045,
        "smartphones/alcatel": 0.045,
        "smartphones/htc": 0.045,
        "smartphones/huawei": 0.045,
        "smartphones/iphone": 0.045,
        "smartphones/lenovo": 0.045,
        "smartphones/lg": 0.045,
        "smartphones/maxcom": 0.045,
        "smartphones/microsoft": 0.045,
        "smartphones/myphone": 0.045,
        "smartphones/nokia": 0.045,
        "smartphones/sony": 0.045,
        "smartphones/sony_ericsson": 0.045,
        "smartphones/motorola": 0.045,
        "smartphones/xiaomi": 0.045,
        "smartphones/other": 0.045,
        "tablets": 0.040,
        "laptops": 0.020,
        "consoles": 0.040,
        "printers": 0.040,
        "monitors": 0.040,
        "mice_and_keyboards": 0.060,
        "routers": 0.060,
        "computer_parts": 0.030,
    },
}

@app.task
def periodic_stonks_finder():
    # Get offers for which stonks has not been checked for more than 1 day (can be changed in config)
    # Only get offers which have a device
    last_stonks_check_before = older_than(minutes=config["stonks"]["older_than"])
    params = {
        "last_stonks_check_before": last_stonks_check_before,
        "has_device": True,
        "is_active": True,
    }
    r = requests.get(f"{API_URL}/v1/offers",
                     params=params)
    offers: List[Offer] = parse_obj_as(List[Offer], r.json())
    print(f"Downloaded {len(offers)} offers with outdated stonks.")

    for offer in offers:
        print(offer.title, offer.device.name)
        find_stonks(offer)


@app.task
def find_stonks(offer: Offer):
    # Get prices for device
    prices = get_prices(offer.device.name)

    if len(prices) == 0:
        logger.info(f"No prices for device {offer.device}")
        update_offer_last_stonks_check(offer)

        return

    prices_amounts = [price.price for price in prices]

    average_price = statistics.median(prices_amounts) * 0.9
    lowest_delivery_price = min([delivery.price for delivery in offer.deliveries], default=10)
    sell_fee = average_price * fees["sell"][offer.category]

    stonks_amount = average_price - offer.price - lowest_delivery_price - sell_fee
    if stonks_amount > 0:
        _fees = [
            FeeCreate(title="Prowizja",
                      amount=sell_fee,
                      currency="PLN")
        ]

        stonks = StonksCreate(stonks_amount=stonks_amount,
                              fees=_fees)

        r = requests.post(f"{API_URL}/v1/offers/{offer.id}/stonks", data=stonks.json())
        r.raise_for_status()

    else:
        update_offer_last_stonks_check(offer)


def get_prices(device_name: str) -> List[Price]:
    params = {
        "newer_than": newer_than(days=config["prices"]["update_older_than"])
    }
    r = requests.get(f"{API_URL}/v1/prices/{device_name}",
                     params=params)

    return parse_obj_as(List[Price], r.json()["prices"]) if r.status_code == 200 else []


def update_offer_last_stonks_check(offer: Offer):
    offer_update_dict = offer.dict(exclude={"last_stonks_check"})
    offer_update_dict = {**offer_update_dict, "last_stonks_check": datetime.utcnow()}
    offer_update = OfferUpdate(**offer_update_dict)
    r = requests.put(f"{API_URL}/v1/offers/{offer.id}", data=offer_update.json())
    r.raise_for_status()
