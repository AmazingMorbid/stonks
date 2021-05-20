import logging

import requests
from requests.auth import HTTPBasicAuth

from allegro_sdk.exceptions import Unauthorized, CouldNotAuthorize
from allegro_sdk.models import Token


LOG_TAG = "auth.py"


def get_token(client_id, client_secret) -> Token:
    logging.info(f"{LOG_TAG} - get_token: Getting token...")

    r = requests.post("https://allegro.pl/auth/oauth/token?grant_type=client_credentials",
                      auth=HTTPBasicAuth(client_id, client_secret))

    if r.status_code == 401:
        logging.error(f"{LOG_TAG} - get_token: Failed while retrieving access token.")
        raise CouldNotAuthorize()

    if r.status_code != 200:
        logging.error(f"{LOG_TAG} - get_token: Failed while retrieving access token.")
        raise requests.HTTPError(r.json())

    logging.info(f"{LOG_TAG} - get_token: Got token.")
    token = Token(**r.json())

    return token
