from allegro_sdk import Allegro
from olx_sdk import OLX

from config import config

allegro = Allegro(config["ALLEGRO_CLIENT_ID"], config["ALLEGRO_CLIENT_SECRET"])

olx = OLX()
