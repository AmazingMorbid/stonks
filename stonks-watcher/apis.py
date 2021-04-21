import os

from allegro_sdk import Allegro
from olx_sdk import OLX

allegro = Allegro(os.getenv("ALLEGRO_CLIENT_ID"),
                  os.getenv("ALLEGRO_CLIENT_SECRET"))
olx = OLX()

