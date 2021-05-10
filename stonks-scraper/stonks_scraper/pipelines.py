import json
import logging
from typing import Optional

import requests
import sentry_sdk
from scrapy import Spider
from scrapy.exceptions import CloseSpider

from stonks_scraper.items import OlxOfferItem
from stonks_types.schemas import OfferCreate

from stonks_scraper.utils.apis import get_device_model, STONKS_API


class OlxOffersPipeline:
    collection_name = "offers"
    LOG_TAG = "OlxOffersPipeline"

    def process_item(self, item: OlxOfferItem, spider: Spider):
        offer = OfferCreate(**dict(item))

        # TODO: move device model extraction to the stonks-watcher and save offers even without it
        # offer.device_name = get_device_model(offer.title)
        #
        # if offer.device_name is None:
        #     logging.error("Device name is None. Currently, stonks watcher is useless without it, so offer won't be saved.")
        #     return item

        try:
            logging.debug(f"Creating new offer id={offer.id}...")
            r = requests.post(f"{STONKS_API}/v1/offers",
                              data=offer.json(),
                              headers={'Content-type': 'application/json'})

            if r.status_code == 409:
                logging.debug(f"Offer id={offer.id} already exists, updating ...")
                r = requests.put(f"{STONKS_API}/v1/offers/{offer.id}",
                                 data=offer.json(),
                                 headers={'Content-type': 'application/json'})
            r.raise_for_status()

            logging.info(f"[{self.LOG_TAG}]: POSTed offer, response: code: {r.status_code}, body: {r.json()}")

        except requests.exceptions.ConnectionError as e:
            sentry_sdk.capture_exception(e)
            logging.exception(f"{self.LOG_TAG}: Could not connect to API. Exiting...\n{e}")

        except requests.HTTPError as e:
            msg = f"{self.LOG_TAG}: Creating an offer failed. Exiting...\n" \
                  f"Exception: {e}\n" \
                  f"Response: {e.response.json()}"
            sentry_sdk.capture_exception(e)
            logging.exception(msg)

        return item
