from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models
from stonks_api.crud.crud import CrudBase


class CrudDevice(CrudBase[models.Device, schemas.DeviceCreate, schemas.DeviceUpdate]):
    def get_one_by_name(self, db: Session, name: str) -> Optional[models.Device]:
        return db.query(models.Device).filter(models.Device.name == name).first()

    def get_many(self,
                 db: Session,
                 skip: int,
                 limit: int,
                 last_price_update_before: Optional[datetime] = None) -> List[models.Device]:
        q = db.query(models.Device)

        if last_price_update_before is not None:
            q = q.filter((models.Device.last_price_update < last_price_update_before) |
                         (models.Device.last_price_update == None))

        devices = q.offset(skip).limit(limit).all()

        return devices

    def create(self,
               db: Session,
               new_model: schemas.DeviceCreate) -> models.Device:
        # Ensure that model **name** is always saved in lowercase.
        new_model.name = new_model.name.lower()
        return super().create(db=db,
                              new_model=new_model)

    def remove_by_name(self,
                       db: Session,
                       name: str):
        db.query(models.Device).filter(models.Device.name == name).delete()
        db.commit()


device = CrudDevice(models.Device)
