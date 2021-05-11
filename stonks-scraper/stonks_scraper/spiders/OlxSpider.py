import logging
from datetime import datetime
from typing import List

import pytz as pytz
import scrapy
import sentry_sdk
from olx_sdk import OLX
from olx_sdk.models import Offer as OlxOffer
from olx_sdk.models import Status as OlxOfferStatus
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse

from stonks_scraper.items import OlxOfferItem
from stonks_types import schemas as stonks_schemas

categories_to_scrap = {
    "elektronika": ["telefony-komorkowe",
                    # "tablety",
                    # "komputery",
                    ]
}
query_params = "?search%5Border%5D=created_at%3Adesc"


class OlxSpider(scrapy.Spider):
    name = "olx_spider"
    allowed_domains = ["olx.pl"]

    start_urls = [f"https://www.olx.pl/{section}/{category}/{query_params}" for section in
                  categories_to_scrap.keys() for category in categories_to_scrap[section]]

    custom_settings = {
        "ITEM_PIPELINES": {
            "stonks_scraper.pipelines.OlxOffersPipeline": 300,
        }
    }

    def __init__(self, *args, **kwargs):
        super(OlxSpider, self).__init__(*args, **kwargs)
        self.olx = OLX()

    def parse(self, response: HtmlResponse, **kwargs):
        offers = response.css("td.offer")[:-1]

        if len(offers) == 0:
            self.logger.critical("No offers in listing had been scraped.")
            return

        self.logger.info(f"Got {len(offers)} offers in listing.")

        for offer in offers:
            offer_id = offer.css("table::attr(data-id)").get()

            self.logger.info(f"Parsing offer <id={offer_id}>")

            if offer_id is None:
                self.logger.critical("Offer id is None.")
                return

            try:
                offer_details: OlxOffer = self.olx.offers.get_details(offer_id)

            except Exception:
                self.logger.error("Could not retrieve data from OLX API.")
                return

            else:
                offer_dict = offer_details.dict()
                offer_item: OlxOfferItem = OlxOfferItem()

                for key in offer_dict.keys() & offer_item.fields.keys() - ["id", "deliveries", "photos"]:
                    offer_item[key] = offer_dict[key]

                offer_item["id"] = f"olx-{offer_details.id}"
                offer_item["category"] = "smartphones"
                offer_item["is_active"] = offer_details.status == OlxOfferStatus.active

                if offer_details.delivery.active:
                    offer_item["deliveries"] = [
                        stonks_schemas.DeliveryCreate(title="Dostawa OLX",
                                                      price=10,
                                                      currency="PLN")
                    ]

                offer_item["photos"] = [photo.link for photo in offer_details.photos]
                offer_item["last_scraped_time"] = datetime.utcnow()

                yield offer_item
