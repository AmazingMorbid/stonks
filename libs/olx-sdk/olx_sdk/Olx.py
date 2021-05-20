import logging
from collections import ChainMap
from pprint import pprint
from typing import List, Dict
from urllib.parse import urljoin

import requests

from olx_sdk import models
from olx_sdk.exceptions import OfferNotFound


class BaseAPI:
    BASE_URL = "https://www.olx.pl/api/v1"
    session: requests.Session = None

    def __init__(self, session: requests.Session):
        self.session = session

    def get(self, url: str) -> requests.Response:
        assert self.session is not None

        url = self.BASE_URL + url
        r = self.session.get(url)

        return r


class Offers(BaseAPI):
    BASE_URL = BaseAPI.BASE_URL + "/offers"

    def get_details(self, offer_id: int) -> models.Offer:
        logging.info(f"Getting details for offer id={offer_id}")

        try:
            r = self.get(f"/{offer_id}")
            r.raise_for_status()
        except requests.HTTPError as e:
            status_code = e.response.status_code

            if status_code == 404:
                raise OfferNotFound(offer_id)

            raise e
        else:
            offer_response: Dict = r.json()["data"]
            offer_params: List[Dict] = offer_response["params"]

            for i, param in enumerate(offer_params):
                param = models.OfferParam(**param)
                if param.key == "price":
                    offer_response["price"] = param.value["value"]
                    offer_response["currency"] = param.value["currency"]
                    offer_response["price_negotiable"] = param.value["negotiable"]
                    offer_response["params"].pop(i)

            photos_dict: List[Dict] = []

            for photo in offer_response["photos"]:
                photo["link"] = photo["link"].split(";")[0]

                photos_dict.append(photo)

            override_dict = {
                "photos": photos_dict,
                "delivery": offer_response["delivery"]["rock"],
            }
            offer: models.Offer = models.Offer(**ChainMap(override_dict, offer_response))

            return offer


class OLX:
    def __init__(self):
        self.session = requests.Session()

        self.offers = Offers(self.session)
