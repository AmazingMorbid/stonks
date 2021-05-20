from datetime import datetime

import scrapy
from olx_sdk import OLX
from olx_sdk.models import Offer as OlxOffer
from olx_sdk.models import Status as OlxOfferStatus
from scrapy.http import HtmlResponse

from stonks_scraper.items import OlxOfferItem
from stonks_types import schemas as stonks_schemas

from stonks_scraper.utils.apis import is_offer_already_scraped

categories_to_scrap = {
    "elektronika": {
        "telefony-komorkowe": {
            "samsung": {},
            "alcatel": {},
            "htc": {},
            "huawei": {},
            "iphone": {},
            "lenovo": {},
            "lg": {},
            "maxcom": {},
            "microsoft": {},
            "myphone": {},
            "nokia": {},
            "sony": {},
            "seony-ericsson": {},
            "motorola": {},
            "xiaomi": {},
            "inne-telefony-gsm": {},
        },
        "tablety": {},
        "komputery": {
            "drukarki-i-skanery": {},
            "akcesoria-i-czesci": {},
            "laptopy": {},
            "monitory": {},
            "myszki-i-klawiatury": {},
            "routery-i-modemy": {},
        },
        "gry-konsole": {
            "konsole": {}
        },
    },
}


def get_category_urls(dic, top=None):
    if not dic:
        yield top

    for key in dic.keys():
        if top is None:
            new_top = f"https://www.olx.pl/{key}"
        else:
            new_top = f"{top}/{key}"

        yield from get_category_urls(dic[key], top=new_top)


query_params = "?search%5Border%5D=created_at%3Adesc"


class OlxSpider(scrapy.Spider):
    name = "olx_spider"
    allowed_domains = ["olx.pl"]

    start_urls = get_category_urls(categories_to_scrap)

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

            if is_offer_already_scraped(offer_id):
                self.logger.info(f"Offer is already scraped. <id={offer_id}>")
                continue

            try:
                offer_details: OlxOffer = self.olx.offers.get_details(offer_id)

            except Exception:
                self.logger.error("Could not retrieve data from OLX API.")
                continue

            else:
                offer_dict = offer_details.dict()
                offer_item: OlxOfferItem = OlxOfferItem()

                for key in offer_dict.keys() & offer_item.fields.keys() - ["id", "deliveries", "photos"]:
                    offer_item[key] = offer_dict[key]

                offer_item["id"] = f"olx-{offer_details.id}"
                offer_item["category"] = category_olx_to_stonks(offer_details.category.id)
                offer_item["is_active"] = offer_details.status == OlxOfferStatus.active

                if offer_details.delivery.active:
                    offer_item["deliveries"] = [
                        stonks_schemas.DeliveryCreate(title="Dostawa OLX",
                                                      price=10,
                                                      currency="PLN")
                    ]

                offer_item["photos"] = [photo.link for photo in offer_details.photos]
                offer_item["scraped_at"] = datetime.utcnow()

                yield offer_item


def category_olx_to_stonks(category_id: int):
    olx_to_stonks_categories = {
        383: "smartphones/samsung",
        1642: "smartphones/alcatel",
        388: "smartphones/htc",
        1483: "smartphones/huawei",
        386: "smartphones/iphone",
        1643: "smartphones/lenovo",
        387: "smartphones/lg",
        1644: "smartphones/maxcom",
        1479: "smartphones/microsoft",
        1645: "smartphones/myphone",
        382: "smartphones/nokia",
        1217: "smartphones/sony",
        384: "smartphones/sony_ericsson",
        385: "smartphones/motorola",
        1646: "smartphones/xiaomi",
        390: "smartphones/other",
        1155: "tablets",
        1199: "laptops",
        1604: "consoles",
        1195: "printers",
        1201: "monitors",
        1203: "mice_and_keyboards",
        1207: "routers",
        1209: "computer_parts",
    }

    return olx_to_stonks_categories[category_id]
