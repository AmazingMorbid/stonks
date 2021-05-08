from typing import List

from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from stonks_types import schemas
from stonks_types.schemas import Device

from stonks_api.tests.utils import delete_devices

device = schemas.DeviceCreate(name="Test device")
device_name_lowercase = device.name.lower()


def test_create_device(client: TestClient):
    delete_devices()
    r = client.post("v1/devices/",
                    data=device.json())
    device_response = Device(**r.json())

    assert r.status_code == 201
    # Ensure that device name is always saved in lowercase
    assert device_response.name == device_name_lowercase
    assert device.dict(exclude={"name"}).items() <= device_response.dict(exclude={"name"}).items()


def test_create_device_already_exists(client: TestClient):
    r = client.post("v1/devices/",
                    data=device.json())

    assert r.status_code == 409


def test_create_device_invalid(client: TestClient):
    r = client.post("v1/devices/", json={"name": "12"})

    assert r.status_code == 422


def test_get_devices(client: TestClient):
    r = client.get("v1/devices/", params={"limit": 500,
                                          "skip": 0})

    assert r.status_code == 200

    devices: List[schemas.Device] = parse_obj_as(List[schemas.Device], r.json())
    device_response = devices[0]
    assert len(devices) == 1
    assert device_response.name == device_name_lowercase
    assert device.dict(exclude={"name"}).items() <= device_response.dict(exclude={"name"}).items()


def test_delete_device(client: TestClient):
    r = client.delete(f"v1/devices/{device_name_lowercase}")

    assert r.status_code == 200
    assert r.json() == {
        "detail": "Device has been deleted."
    }

    r = client.get("v1/devices")
    assert len(r.json()) == 0


def test_delete_device_not_found(client: TestClient):
    r = client.delete(f"v1/devices/THIS DOES NOT EXIST")

    assert r.status_code == 404
    assert r.json() == {
        "detail": "Device not found."
    }
