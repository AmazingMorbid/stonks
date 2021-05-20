import os

import yaml
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = {}

with open("config/config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)

    except yaml.YAMLError as exc:
        print(exc)

API_URL = config["api_url"]
DEVICE_RECOGNIZER_API = config["device_recognizer_api"]
config["ALLEGRO_CLIENT_ID"] = os.getenv("ALLEGRO_CLIENT_ID")
config["ALLEGRO_CLIENT_SECRET"] = os.getenv("ALLEGRO_CLIENT_SECRET")

if config["ALLEGRO_CLIENT_ID"] is None or config["ALLEGRO_CLIENT_SECRET"] is None:
    raise ValueError("ALLEGRO_CLIENT_ID and ALLEGRO_CLIENT_SECRET not specified.")
