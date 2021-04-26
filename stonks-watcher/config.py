import os

from allegro_sdk import Allegro
from dotenv import load_dotenv, find_dotenv
from olx_sdk import OLX

load_dotenv(find_dotenv())

API_URL = os.getenv("API_URL", "http://localhost:8000")
OFFER_UPDATE_INTERVAL = os.getenv("OFFER_UPDATE_INTERVAL", 1)
OFFER_UPDATE_OLDER_THAN = os.getenv("OFFER_UPDATE_OLDER_THAN", 30)

ALLEGRO_CLIENT_ID = os.getenv("ALLEGRO_CLIENT_ID")
ALLEGRO_CLIENT_SECRET = os.getenv("ALLEGRO_CLIENT_SECRET")

if ALLEGRO_CLIENT_ID is None or ALLEGRO_CLIENT_SECRET is None:
    raise ValueError("ALLEGRO_CLIENT_ID and ALLEGRO_CLIENT_SECRET not specified.")

allegro = Allegro(ALLEGRO_CLIENT_ID, ALLEGRO_CLIENT_SECRET)

olx = OLX()
