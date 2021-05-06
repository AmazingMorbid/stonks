import unittest

import responses
from olx_sdk.Olx import Offers

from stonks_scraper.spiders.OlxSpider import OlxSpider


class OlxSpiderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = OlxSpider()

    @responses.activate
    def test_parse_details(self):
        print(f"{Offers.BASE_URL}/669683013")
        responses.add(responses.GET, f"{Offers.BASE_URL}/669683013", json=)
        details = self.spider.parse_details(None, offer_id=669683013)
        #
        print(details)


if __name__ == '__main__':
    unittest.main()
