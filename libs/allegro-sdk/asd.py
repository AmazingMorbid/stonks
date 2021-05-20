# import json
# import os
# from typing import Optional
#
# from dotenv import load_dotenv
#
# from allegro_sdk import Allegro
# from allegro_sdk.exceptions import Unauthorized
# from allegro_sdk.models import Token
#
# load_dotenv()
#
#
# def load_token() -> Optional[Token]:
#     print("Loading token from file...")
#     try:
#         with open("token.json", "r") as f:
#             token: Token = json.load(f)
#             return token
#     except FileNotFoundError:
#         print("Token not found.")
#         return None
#
#
# def save_token(token: Token):
#     print("Saving token to file...")
#     with open("token.json", "w") as f:
#         json.dump(token.dict(), f)
#
#
# try:
#
#     allegro = Allegro(client_id=os.getenv("ALLEGRO_CLIENT_ID"),
#                       client_secret=os.getenv("ALLEGRO_CLIENT_SECRET"),
#                       token=load_token(),
#                       # on_token_acquired=save_token,
#                       )
# except Unauthorized as e:
#     print(e)
# else:
#     print(allegro.offers.check_get())
import json
import logging
import os
from pprint import pprint

from allegro_sdk import Allegro
from dotenv import load_dotenv

root = logging.getLogger()
root.setLevel(logging.INFO)


load_dotenv()

allegro = Allegro(os.getenv("ALLEGRO_CLIENT_ID"),
                  os.getenv("ALLEGRO_CLIENT_SECRET"))

# offers = allegro.offers.listing(**{"category.id": 165,
#                                    "phrase": "pixel 3a",
#                                    "include": ["-all", "items"],
#                                    "sellingMode.format": "BUY_NOW",
#                                    "limit": 60,
#                                    "sort": "-startTime",
#                                    "offset": 0,
#                                    "parameter.11323": "11323_2"})
# pprint(offers.json())
# pprint(offers.text)

# pprint(offers)
categories = allegro.sale.categories()

pprint(categories)

# with open("/home/lomber/Desktop/category.json", "w+") as f:
#     json.dump(categories, f, indent=4)
