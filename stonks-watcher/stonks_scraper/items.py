from scrapy import Item, Field


class OlxOfferItem(Item):
    id = Field()
    url = Field()

    title = Field()
    description = Field()
    category = Field()

    price = Field()
    currency = Field()

    deliveries = Field()

    photos = Field()

    last_refresh_time = Field()
    last_scraped_time = Field()
