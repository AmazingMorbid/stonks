from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models


def get_many(db: Session,
             limit: int = 500,
             skip: int = 0,
             last_price_update_before: Optional[datetime] = None) -> List[models.Device]:
    q = db.query(models.Device)

    if last_price_update_before is not None:
        q = q.filter((models.Device.last_price_update < last_price_update_before) |
                     (models.Device.last_price_update == None))

    devices = q.offset(skip).limit(limit).all()

    return devices


def get_one_by_name(db: Session, device_name: str) -> Optional[models.Device]:
    return db.query(models.Device).filter(models.Device.name == device_name).first()


def create(db: Session, device: schemas.DeviceCreate) -> models.Device:
    device.name = device.name.lower()
    db_device = models.Device(**device.dict())

    db.add(db_device)
    db.flush()
    db.refresh(db_device)

    db.commit()

    return db_device


def delete_by_name(db: Session,
                   device_name: str):
    db.query(models.Device).filter(models.Device.name == device_name).delete()
    db.commit()
