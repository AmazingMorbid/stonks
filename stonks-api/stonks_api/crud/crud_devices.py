from typing import Optional, List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models


def get_many(db: Session,
             limit: int = 500,
             skip: int = 0) -> List[models.Device]:
    devices = db.query(models.Device).offset(skip).limit(limit).all()

    return devices


def get_one_by_name(db: Session, device_name: str):
    return db.query(models.Device).filter(models.Device.name == device_name).first()


def create_prices(db: Session,
                  device_name: str,
                  prices: List[schemas.PriceCreate]):
    db_prices = [models.Price(**price.dict(),
                              device_name=device_name) for price in prices]
    db.add_all(db_prices)
    db.commit()


def create(db: Session, device: schemas.DeviceCreate) -> models.Device:
    device_dict = device.dict()
    device_dict.pop("price")
    db_device = models.Device(**device_dict)

    db.add(db_device)
    db.flush()
    db.refresh(db_device)

    if device.price is not None:
        create_prices(db=db,
                      device_name=db_device.name,
                      prices=device.price)

    db.commit()

    return db_device


def delete_by_name(db: Session,
                   device_name: str):
    db.query(models.Device).filter(models.Device.name == device_name).delete()
    db.commit()
