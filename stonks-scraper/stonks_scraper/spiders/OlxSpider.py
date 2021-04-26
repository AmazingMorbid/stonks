from datetime import datetime
from typing import List

import pytz as pytz
import scrapy
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
    LOG_TAG = "OlxSpider"

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
        for offer in response.css("td.offer")[:-1]:
            # offer_item = OlxOfferItem()

            # offer_item["title"] = offer.xpath('div/table/tbody/tr[1]/td[2]/div/h3/a/strong/text()').get()
            # offer_item["price"] = convert_price(offer.css("p.price>strong::text").get(), website="olx")
            # offer_item["currency"] = "PLN"
            # offer_item["url"] = offer.xpath('div/table/tbody/tr[1]/td[2]/div/h3/a/@href').get()
            # offer_item["scraped_date"] = datetime.now()

            # request = scrapy.Request(
            #     offer_item["url"],
            #     callback=self.parse_details,
            #     cb_kwargs={"item": offer_item}
            # )

            url = offer.xpath('div/table/tbody/tr[1]/td[2]/div/h3/a/@href').get()

            if url is None:
                raise CloseSpider(reason=f"{self.LOG_TAG}: Offer url is None.")

            request = scrapy.Request(
                url,
                callback=self.parse_details,
            )

            yield request

    def parse_details(self, response: HtmlResponse, offer_id=None):
        # item["offer_id"] = response.xpath('//ul[@class="offer-bottombar__items"]/li[3]//strong/text()').get()
        # item["description"] = "\n".join(response.css("div#textContent::text").getall()).strip()
        # added_datetime = response.xpath('//ul[@class="offer-bottombar__items"]/li[1]//strong/text()').get()[1:]
        # item["added_date"] = dateparser.parse(added_datetime, languages=["pl"])
        #
        # r = requests.get(f"https://www.olx.pl/api/v1/offers/{item['offer_id']}")
        # print(r.json())
        #
        # yield item

        if offer_id is None:
            offer_id = response.xpath('//ul[@class="offer-bottombar__items"]/li[3]//strong/text()').get()

        if offer_id is None:
            raise CloseSpider(reason=f"{self.LOG_TAG}: Offer id is None.")

        try:
            offer: OlxOffer = self.olx.offers.get_details(offer_id)
        except Exception as e:
            raise CloseSpider(reason=repr(e))

        else:
            offer_dict = offer.dict()
            offer_item: OlxOfferItem = OlxOfferItem()

            for key in offer_dict.keys() & offer_item.fields.keys() - ["id", "deliveries", "photos"]:
                offer_item[key] = offer_dict[key]

            offer_item["id"] = f"olx-{offer.id}"
            offer_item["category"] = "smartphones"
            offer_item["is_active"] = offer.status == OlxOfferStatus.active

            if offer.delivery.active:
                offer_item["deliveries"] = [
                    stonks_schemas.DeliveryCreate(title="Dostawa OLX",
                                                  price=10,
                                                  currency="PLN")
                ]

            offer_item["photos"] = [photo.link for photo in offer.photos]
            offer_item["last_scraped_time"] = datetime.now(pytz.utc)

            return offer_item
