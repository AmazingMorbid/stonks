import pytest
from pytest import Session
from fastapi.testclient import TestClient

from main import app
from stonks_api.tests.utils import delete_data


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def pytest_sessionstart(session: Session):
    delete_data()


def pytest_sessionfinish(session: Session):
    delete_data()
