import logging

import requests
from scrapy import Spider

from stonks_scraper.items import OlxOfferItem
from stonks_types.schemas import OfferCreate

from stonks_scraper.utils.apis import STONKS_API


class OlxOffersPipeline:
    logger = logging.getLogger("olx_offers_pipeline")

    def process_item(self, item: OlxOfferItem, spider: Spider):
        offer = OfferCreate(**dict(item))

        self.logger.info(f"Processing offer <id={offer.id}>")

        # TODO: move device model extraction to the stonks-watcher and save offers even without it
        # offer.device_name = get_device_model(offer.title)
        #
        # if offer.device_name is None:
        #     logging.error("Device name is None. Currently, stonks watcher is useless without it, so offer won't be saved.")
        #     return item

        try:
            self.logger.debug(f"Creating new offer id={offer.id}...")
            r = requests.post(f"{STONKS_API}/v1/offers",
                              data=offer.json(),
                              headers={'Content-type': 'application/json'})

            # if r.status_code == 409:
            #     self.logger.debug(f"Offer id={offer.id} already exists, updating ...")
            #     r = requests.put(f"{STONKS_API}/v1/offers/{offer.id}",
            #                      data=offer.json(),
            #                      headers={'Content-type': 'application/json'})
            r.raise_for_status()

        except requests.HTTPError as e:
            msg = f"Creating an offer failed. Exiting...\n" \
                  f"Exception: {e}\n" \
                  f"Response: {e.response.json()}"
            self.logger.error(msg)
            return

        except requests.exceptions.ConnectionError:
            self.logger.error(f"Could not connect to the stonks API.")
            return

        except requests.exceptions.Timeout:
            self.logger.error(f"Timed out while connecting to the stonks API.")
            return

        return item
