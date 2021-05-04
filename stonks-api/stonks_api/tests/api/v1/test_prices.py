from fastapi.testclient import TestClient
from stonks_types.schemas import PriceCreate, PricesCreate, Prices

prices: PricesCreate = PricesCreate(prices=[
    PriceCreate(source="test source",
                price=69,
                currency="PLN")
])


def test_create_prices(client: TestClient):
    r = client.post(f"/v1/prices/test device", data=prices.json())
    response_prices: Prices = Prices(**r.json())

    assert r.status_code == 201

    price = prices.prices[0]
    response_price = response_prices.prices[0]

    assert price.dict(exclude={"date"}).items() == response_price.dict(exclude={"date", "id"}).items()


def test_create_prices_device_not_found(client: TestClient):
    r = client.post(f"/v1/prices/THIS DOES NOT EXIST", data=prices.json())

    assert r.status_code == 404


def test_get_prices_for_device(client: TestClient):
    r = client.get(f"/v1/prices/test device")
    response_prices: Prices = Prices(**r.json())

    assert r.status_code == 200

    price = prices.prices[0]
    response_price = response_prices.prices[0]

    assert price.dict(exclude={"date"}).items() == response_price.dict(exclude={"date", "id"}).items()


def test_get_prices_for_device_not_found(client: TestClient):
    r = client.get(f"/v1/prices/HIS DOES NOT EXIST")

    assert r.status_code == 404
