from scrapy import Item, Field
from scrapy.utils.display import pformat


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
    is_active = Field()

    last_refresh_time = Field()
    last_scraped_time = Field()

    def __repr__(self):
        keys_to_show = {"id", "title", "url"}
        _dict = dict(self)
        # pformat returns a pretty string of dictionary
        # print only selected fields
        return pformat({key: _dict[key] for key in _dict.keys() & keys_to_show})
