# from tasks import update_offers
#
# job = update_offers()
# result = job.apply_async()
# print(result.ready())
# print(result.get())
# print(result.successful())

# import logging
# from datetime import datetime, timedelta
# from time import sleep
# from typing import List
#
# import requests
# from celery import Celery, group
# from pydantic import parse_obj_as
#
# from stonks_types.schemas import Offer, OfferUpdate
# from olx_sdk.models import Offer as OlxOffer
#
# # import sentry_sdk
# # from sentry_sdk.integrations.celery import CeleryIntegration
#
# from config import API_URL, olx
#
# older_than_datetime = (datetime.now() - timedelta(minutes=30)).isoformat()
#
# r = requests.get(f"{API_URL}/v1/offers", params={"older_than": older_than_datetime})
# offers: List[Offer] = parse_obj_as(List[Offer], r.json())
#
# for offer in offers:
#     print(f"Downloading offer {offer.id}")
#     olx_offer: OlxOffer = olx.offers.get_details(offer.id.split("-")[1])
#
#     print(olx_offer.status)
import json
import statistics
import time
from typing import List

import requests
from olx_sdk.models import Offer as OlxOffer
from pydantic import parse_obj_as
from stonks_types.schemas import Offer, Fee, FeeCreate, StonksCreate

from config import olx

# with open("olx_offer.json", "r") as f:
#     offer = OlxOffer(**json.load(f))

offer_response = requests.get(f"http://localhost:8000/v1/offers/")
offers: List[Offer] = parse_obj_as(List[Offer], offer_response.json())

from config import allegro

broken_flags = "-uszko* -pęknię*"

for offer in offers:
    time.sleep(1)
    allegro_offers = allegro.offers.listing(**{"category.id": 165,
                                               "phrase": f"{offer.title} {broken_flags}",
                                               "include": ["-all", "items"],
                                               "sellingMode.format": "BUY_NOW",
                                               "limit": 60,
                                               "sort": "+price",
                                               "offset": 0,
                                               "parameter.11323": "11323_2",
                                               "fallback": False})

    if len(allegro_offers) > 0:
        prices = [allegro_offer.sellingMode.price.amount for allegro_offer in allegro_offers]

        harmonic_price = statistics.harmonic_mean(prices)

        sell_fee = FeeCreate(title="Opłata od sprzedaży",
                             amount=0.045 * harmonic_price,
                             currency="PLN")

        total_buy = offer.price

        if len(offer.deliveries) > 0:
            total_buy += offer.deliveries[0].price
        else:
            total_buy += 15

        total_sell = harmonic_price - sell_fee.amount

        if total_sell > total_buy:
            stonks = StonksCreate(low_price=min(prices),
                                  high_price=max(prices),
                                  median_price=statistics.median(prices),
                                  average_price=statistics.mean(prices),
                                  harmonic_price=harmonic_price,
                                  fees=[sell_fee]
                                  )

            r = requests.post(f"http://localhost:8000/v1/offers/{offer.id}/stonks", data=stonks.json())

            print(r.json())
            print(r.status_code)

