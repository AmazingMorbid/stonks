# from enum import Enum
# from typing import List, Callable, Optional
#
# import requests
# from requests.auth import HTTPBasicAuth
#
# from allegro_sdk.exceptions import Unauthorized, CouldNotAuthorize
# from allegro_sdk.models import Token
#
#
# # class BaseAPI:
# #     BASE_URL = "https://api.allegro.pl"
# #     session: requests.Session = None
# #
# #     def __init__(self, session: requests.Session):
# #         self.session = session
# #
# #     def get(self, url: str):
# #         print(self.session.headers.get("Authorization"))
# #         print(self.BASE_URL + url)
# #         return self.session.get(self.BASE_URL + url)
#
#
# # class SearchMode(str, Enum):
# #     regular = "REGULAR"
# #     descriptions = "DESCRIPTIONS"
# #     closed = "CLOSED"
# #
# #
# # class Offers(BaseAPI):
# #
# #     def listing(self,
# #                 category_id: str,
# #                 search_mode: SearchMode,
# #                 offset: int,
# #                 limit: int,
# #                 sort: str,
# #                 include: List[str]):
# #         pass
# #
# #     def check_get(self):
# #         return self.get("/offers/listing?category.id=77917&include=-all&include=items")
# #
#
# class AllegroAuth:
#     def __init__(self,
#                  client_id,
#                  client_secret):
#         self.client_id = client_id
#         self.client_secret = client_secret
#
#     def get_token(self) -> Token:
#         r = requests.post("https://allegro.pl/auth/oauth/token?grant_type=client_credentials",
#                           auth=HTTPBasicAuth(self.client_id, self.client_secret))
#
#         if r.status_code == 401:
#             raise Unauthorized()
#
#         if r.status_code != 200:
#             raise requests.HTTPError(r.json())
#
#         token = Token(**r.json())
#
#         return token
#
#
# class BaseApi:
#     BASE_URL = ""
#
#     def __init__(self, client_id, client_secret):
#         self.auth = AllegroAuth(client_id, client_secret)
#
#         self.session: requests.Session = requests.Session()
#         self.session.headers.update({"Accept": "application/vnd.allegro.public.v1+json"})
#
#     def get(self, route: str, params: ) -> requests.Response:
#         url = self.BASE_URL + route
#
#         return self._make_request(method="GET",
#                                   url=url,
#                                   params=)
#
#     def _make_request(self, **kwargs):
#         # Get number of tries and remove it from kwargs,
#         # this way you can pass them to session.request
#         _tries: int = kwargs.pop("tries", 0)
#
#         try:
#             r = self.session.request(**kwargs)
#             r.raise_for_status()
#         except requests.exceptions.HTTPError as e:
#             status_code: int = e.response.status_code
#
#             if status_code == 401:
#                 if _tries >= 0:
#                     raise CouldNotAuthorize()
#
#                 self.refresh_token()
#                 self._make_request(tries=_tries+1, **kwargs)
#
#             raise e.__class__(e.response.json())
#         else:
#             return r
#
#     def refresh_token(self):
#         token = self.auth.get_token()
#         self.session.headers.update({"Authorization": token.access_token})
#
#
# class Offers:
#     def __init__(self, client: BaseApi):
#         self.client = client
#
#     def listing(self):
#         return self.client.get("/listing")
#
#
# class Allegro(BaseApi):
#     def __init__(self,
#                  client_id: str,
#                  client_secret: str,
#                  token: Optional[Token] = None):
#         """
#         :param client_id: found in Allegro Developer Portal dashboard
#         :param client_secret: found in Allegro Developer Portal dashboard
#         :param token: This token is going to be checked on startup.
#                       If it is valid, it will be used for requests, if not, a new one will be requested.
#         """
#         super(Allegro, self).__init__(client_id, client_secret)
#
#         self.offers = Offers(self)
