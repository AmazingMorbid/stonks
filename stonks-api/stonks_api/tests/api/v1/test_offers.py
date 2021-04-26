from datetime import datetime
from typing import List

from fastapi.testclient import TestClient
from pydantic import parse_obj_as, BaseModel
from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models
from stonks_api.database import SessionLocal

data_offer_create = schemas.OfferCreate(id="test_offer",
                                        url="https://example.org",
                                        title="Example title",
                                        description="Example description",
                                        category="smartphone",
                                        price=500.59,
                                        currency="PLN",
                                        photos=[
                                            "https://example.image.org"
                                        ],
                                        last_refresh_time=datetime.now(),
                                        last_scraped_time=datetime.now(),
                                        is_active=True)
deliveries: List[schemas.DeliveryCreate] = [
    schemas.DeliveryCreate(title="test delivery",
                           price=9.99,
                           currency="PLN")
]


def delete_offers():
    db: Session = SessionLocal()
    db.query(models.Offer).delete()
    db.commit()
    db.close()


# CREATE OFFER
def test_create_offer(client: TestClient):
    delete_offers()

    r = client.post(f"/v1/offers/", data=data_offer_create.json())

    assert r.status_code == 201

    offer = schemas.Offer(**r.json())
    assert offer.deliveries == []

    sent_offer_dict = data_offer_create.dict()
    sent_offer_dict["deliveries"] = []

    sent_offer = schemas.Offer(**sent_offer_dict)
    assert offer == sent_offer


def test_create_offer_error(client: TestClient):
    r = client.post(f"/v1/offers/", data={})

    assert r.status_code == 422


def test_create_offer_already_exists(client: TestClient):
    r = client.post(f"/v1/offers/", data=data_offer_create.json())

    assert r.status_code == 409


# UPDATE OFFER
def test_update_offer(client: TestClient):
    offer_update = schemas.OfferUpdate(**data_offer_create.dict())
    offer_update.title = "edited title"

    r = client.put(f"/v1/offers/test_offer", data=offer_update.json())

    assert r.status_code == 200

    offer = schemas.Offer(**r.json())

    assert offer.title == "edited title"


def test_update_offer_not_found(client: TestClient):
    offer_update = schemas.OfferUpdate(**data_offer_create.dict())
    offer_update.title = "edited title"

    r = client.put(f"/v1/offers/THIS DOES NOT EXIST", data=offer_update.json())

    assert r.status_code == 404
    assert r.json()["detail"] == "Offer not found"


def test_update_offer_invalid(client: TestClient):
    r = client.put(f"/v1/offers/edited title", data={})

    assert r.status_code == 422


# GET OFFER
def test_get_offer(client: TestClient):
    r = client.get(f"/v1/offers/test_offer")

    assert r.status_code == 200
    offer = schemas.Offer(**r.json())
    assert offer.title == "edited title"


def test_get_offer_not_found(client: TestClient):
    r = client.get(f"/v1/offers/THIS DOES NOT EXIST")

    assert r.status_code == 404


# GET OFFERS
def test_get_offers(client: TestClient):
    r = client.get(f"/v1/offers")

    assert r.status_code == 200

    offers = parse_obj_as(List[schemas.Offer], r.json())

    assert len(offers) > 0


def test_delete_offer(client: TestClient):
    r = client.delete(f"/v1/offers/test_offer")

    assert r.status_code == 200
    assert r.json() == {
        "detail": "Offer had been deleted"
    }


def test_delete_offer_not_found(client: TestClient):
    r = client.delete(f"/v1/offers/THIS DOES NOT EXIST")

    assert r.status_code == 404


# DELIVERIES
def test_create_offer_with_deliveries(client: TestClient):
    delete_offers()

    offer_create = data_offer_create
    offer_create.deliveries = deliveries

    r = client.post(f"/v1/offers/", data=offer_create.json())

    assert r.status_code == 201

    offer = schemas.Offer(**r.json())

    assert offer.deliveries[0].id is not None
    assert schemas.OfferCreate(**offer.dict()) == offer_create


class DeliveryCreateList(BaseModel):
    __root__: List[schemas.DeliveryCreate]


delivery = schemas.DeliveryCreate(title="testowa oferta 2",
                                  price=69.9,
                                  currency="PLN")
delivery_create = DeliveryCreateList(__root__=[delivery])


def test_create_delivery(client: TestClient):
    r = client.post(f"/v1/offers/test_offer/deliveries", data=delivery_create.json())

    assert r.status_code == 201

    deliveries = parse_obj_as(List[schemas.Delivery], r.json())

    for delivery in deliveries:
        assert delivery.id is not None


def test_create_delivery_not_found(client: TestClient):
    print(delivery_create.json())
    r = client.post(f"/v1/offers/THIS DOESNT EXIST/deliveries", data=delivery_create.json())

    assert r.status_code == 404


def test_create_delivery_invalid(client: TestClient):
    r = client.post(f"/v1/offers/test_offer/deliveries", json={})

    assert r.status_code == 422


test_deliveries: List[schemas.Delivery]


def test_get_deliveries(client: TestClient):
    global test_deliveries
    r = client.get(f"/v1/offers/test_offer/deliveries")

    assert r.status_code == 200

    test_deliveries = parse_obj_as(List[schemas.Delivery], r.json())

    assert test_deliveries is not None
    assert len(test_deliveries) > 0


def test_get_deliveries_not_found(client: TestClient):
    r = client.get(f"/v1/offers/THIS DOES NOT EXIST/deliveries")

    assert r.status_code == 404


delivery_update = schemas.DeliveryUpdate(title="updated delivery",
                                         price=5.6,
                                         currency="PLN")


def test_update_delivery(client: TestClient):
    global test_deliveries
    test_delivery = test_deliveries[0]

    r = client.put(f"/v1/offers/test_offer/deliveries/{test_delivery.id}", data=delivery_update.json())

    assert r.status_code == 200

    response_delivery = schemas.Delivery(**r.json())

    assert response_delivery.id is not None

    print(response_delivery)
    print(test_delivery)

    assert schemas.DeliveryCreate(**response_delivery.dict()) == delivery_update


def test_update_delivery_invalid(client: TestClient):
    global test_deliveries
    test_delivery = test_deliveries[0]

    r = client.put(f"/v1/offers/test_offer/deliveries/{test_delivery.id}", data={})

    assert r.status_code == 422


def test_update_delivery_offer_not_found(client: TestClient):
    print(delivery_update.json())
    r = client.put(f"/v1/offers/THIS DOES NOT EXIST/deliveries/-1", data=delivery_update.json())

    assert r.status_code == 404


def test_update_delivery_delivery_not_found(client: TestClient):
    r = client.put(f"/v1/offers/test_offer/deliveries/-1", data=delivery_update.json())

    assert r.status_code == 404


def test_delete_deliveries(client: TestClient):
    r = client.delete(f"/v1/offers/test_offer/deliveries")

    assert r.status_code == 200
    assert r.json() == {"message": f"Deliveries for offer test_offer had been deleted."}


def test_delete_deliveries_offer_not_found(client: TestClient):
    r = client.delete(f"/v1/offers/THIS DOES NOT EXIST/deliveries")

    assert r.status_code == 404
