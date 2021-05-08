import logging
from pprint import pprint
from typing import List, Optional, Generator

import requests

from urllib.parse import urljoin

from pydantic.tools import parse_obj_as

from allegro_sdk import auth, models
from allegro_sdk.exceptions import CouldNotAuthorize


class AllegroSession(requests.Session):
    LOG_TAG = "[AllegroSession]"

    def __init__(self, client_id, client_secret):
        super(AllegroSession, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret

        self.headers.update({"Accept": "application/vnd.allegro.public.v1+json"})

        self.update_token()

    def update_token(self):
        logging.info(f"{self.LOG_TAG}: Updating token.")
        token = auth.get_token(self.client_id, self.client_secret)
        self.headers.update({"Authorization": f"Bearer {token.access_token}"})

    def get(self, url, **kwargs) -> requests.Response:
        # Get number of tries and remove it from kwargs,
        # this way you can pass them to session.request
        _tries: int = kwargs.pop("tries", 0)

        logging.info(f"{self.LOG_TAG}: GET request...")
        try:
            r = super().get(url, **kwargs)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logging.debug(f"{self.LOG_TAG} - self.get: Access token probably expired.")

                if _tries >= 10:
                    logging.error(f"{self.LOG_TAG} - self.get: Could not retrieve access token.")
                    raise CouldNotAuthorize()

                self.update_token()
                self.get(url, tries=_tries + 1, **kwargs)
            else:
                raise e.__class__(e.response.json())
        else:
            logging.info(f"{self.LOG_TAG} - self.get: Got response.")
            return r


class BaseApi:
    BASE_URL = "https://api.allegro.pl"

    def __init__(self, session: AllegroSession):
        self.session = session

    def url(self, route: str):
        return urljoin(self.BASE_URL, route)


class Sale(BaseApi):
    LOG_TAG = "Sale"

    def categories(self, parent_id: str = None) -> List[models.Category]:
        logging.info(f"{self.LOG_TAG}: Getting category info (id: {parent_id})")

        r = self.session.get(self.url("/sale/categories"), params={"parent.id": parent_id})
        categories = parse_obj_as(List[models.Category], r.json()["categories"])

        return categories


class Offers(BaseApi):
    LOG_TAG = "Offers"

    def listing(self, **kwargs) -> List[models.Offer]:
        logging.info(f"{self.LOG_TAG}: Getting listing...")

        r = self.session.get(self.url("/offers/listing"), params=kwargs)
        items = r.json()["items"]
        offers = parse_obj_as(List[models.Offer], items["regular"] + items["promoted"])

        return offers


class Allegro:
    def __init__(self, client_id, client_secret):
        self.session = AllegroSession(client_id, client_secret)

        self.offers = Offers(self.session)
        self.sale = Sale(self.session)
