import json
import logging
from typing import Optional

import requests
from scrapy import Spider
from scrapy.exceptions import CloseSpider

from stonks_scraper.items import OlxOfferItem
from stonks_types.schemas import OfferCreate, DeviceCreate


class OlxOffersPipeline:
    collection_name = "offers"
    LOG_TAG = "OlxOffersPipeline"

    def process_item(self, item: OlxOfferItem, spider: Spider):
        offer = OfferCreate(**dict(item))

        # Get model for device
        r = requests.get("http://localhost:8880/api/v1/get-info", params={"text": offer.title})

        if r.status_code == 200:
            if (device_info := r.json()) is not None:
                device_model: Optional[str] = device_info["model"]

                if device_model is not None and len(device_model) > 2:
                    device_model = device_model.lower()
                    device = DeviceCreate(name=device_model)
                    r = requests.post("http://localhost:8000/v1/devices", data=device.json())

                    if r.status_code == 201 or r.status_code == 409:
                        # If device was created successfully (or 409 already exists), assign it to the offer
                        offer.device = device_model

        try:
            r = requests.post("http://localhost:8000/v1/offers",
                              data=offer.json(),
                              headers={'Content-type': 'application/json'})

            if r.status_code == 409:
                r = requests.put(f"http://localhost:8000/v1/offers/{offer.id}",
                                 data=offer.json(),
                                 headers={'Content-type': 'application/json'})
            r.raise_for_status()

            logging.info(f"[{self.LOG_TAG}]: POSTed offer, response: code: {r.status_code}, body: {r.json()}")
        except requests.exceptions.ConnectionError:
            raise CloseSpider(reason=f"{self.LOG_TAG}: Could not connect to API. Exiting...")

        except requests.HTTPError as e:
            raise CloseSpider(reason=f"{self.LOG_TAG}: Creating an offer failed. Exiting...")

        return item
