import os

OFFER_DOWNLOAD_INTERVAL = os.getenv("OFFER_DOWNLOAD_INTERVAL", 1)
OFFER_UPDATE_INTERVAL = os.getenv("OFFER_UPDATE_INTERVAL", 1)
OFFER_UPDATE_OLDER_THAN = os.getenv("OFFER_UPDATE_OLDER_THAN", 30)

from olx_sdk import OLX
from allegro_sdk import Allegro
from stonks_types.schemas import Offer

olx = OLX()
print(olx.offers.get_details(671944915))
