from pprint import pprint

import requests

from olx_sdk import OLX

olx = OLX()
offer = olx.offers.get_details(673413468)
pprint(offer)
