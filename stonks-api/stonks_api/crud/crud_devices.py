from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models


def get_many(db: Session,
             limit: int = 500,
             skip: int = 0,
             device_name: str = None,
             last_price_update_before: Optional[datetime] = None) -> List[models.Device]:
    q = db.query(models.Device)

    if device_name is not None:
        q = q.filter(models.Device.name == device_name)

    if last_price_update_before is None:
        q = q.filter(models.Device.last_price_update > datetime.utcnow() - timedelta(days=7))
    else:
        q = q.filter((models.Device.last_price_update < last_price_update_before) |
                     (models.Device.last_price_update == None))

    devices = q.offset(skip).limit(limit).all()

    return devices


def get_one_by_name(db: Session, device_name: str) -> Optional[models.Device]:
    return db.query(models.Device).filter(models.Device.name == device_name).first()


def create_prices(db: Session,
                  device_name: str,
                  prices: List[schemas.PriceCreate]) -> List[models.Price]:
    db_prices = [models.Price(**price.dict(),
                              device_name=device_name) for price in prices]
    db.add_all(db_prices)
    db.commit()
    [db.refresh(db_price) for db_price in db_prices]

    return db_prices


def create(db: Session, device: schemas.DeviceCreate) -> models.Device:
    device.name = device.name.lower()
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
