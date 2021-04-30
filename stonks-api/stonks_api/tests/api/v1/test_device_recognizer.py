from fastapi.testclient import TestClient


def test_get_device_info(client: TestClient):
    r = client.get("v1/device-recognizer", params={"text": "Apple iPhone X 64 GB Space Gray"})

    assert r.status_code == 200
    assert r.json() == {
        "model": "Apple iPhone X",
        "color": "Space Gray",
        "memory": None,
        "storage": "64 GB",
        "screen_size": None
    }
