from typing import List

from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from stonks_types import schemas

from stonks_api.tests.utils import delete_stonks

fees: List[schemas.FeeCreate] = [
    schemas.FeeCreate(title="test fee",
                      amount=10.5,
                      currency="PLN"),
]
stonks_create: schemas.StonksCreate = schemas.StonksCreate(stonks_amount=100,
                                                           fees=fees)


stonks_response: schemas.Stonks


def test_create_stonks(client: TestClient):
    global stonks_response

    delete_stonks()

    r = client.post(f"/v1/offers/test_offer/stonks", data=stonks_create.json())

    assert r.status_code == 201

    response_stonks = schemas.Stonks(**r.json())

    assert response_stonks.id is not None
    assert response_stonks.fees[0].id is not None
    assert schemas.StonksCreate(**response_stonks.dict()) == stonks_create

    stonks_response = response_stonks


def test_create_stonks_offer_not_found(client: TestClient):
    r = client.post(f"/v1/offers/THIS DOES NOT EXIST/stonks", data=stonks_create.json())

    assert r.status_code == 404


def test_get_stonkses(client: TestClient):
    r = client.get(f"/v1/stonks")

    assert r.status_code == 200

    stonkses = parse_obj_as(List[schemas.Stonks], r.json())

    assert len(stonkses) > 0


def test_get_stonks(client: TestClient):
    r = client.get(f"/v1/stonks/{stonks_response.id}")

    assert r.status_code == 200

    stonks = schemas.Stonks(**r.json())

    assert stonks == stonks_response


def test_get_stonks_not_found(client: TestClient):
    r = client.get(f"/v1/stonks/-1")

    assert r.status_code == 404


def test_delete_stonks(client: TestClient):
    r = client.delete(f"/v1/stonks/{stonks_response.id}")

    assert r.status_code == 200
    assert r.json() == {
        "detail": "Stonks has been deleted."
    }

    r = client.get(f"/v1/stonks/{stonks_response.id}")
    assert r.status_code == 404


def test_delete_stonks_not_found(client: TestClient):
    r = client.delete(f"/v1/stonks/-1")

    assert r.status_code == 404
