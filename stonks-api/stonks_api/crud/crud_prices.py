import logging
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models
from stonks_api.crud.crud import CrudBase


class CrudPrices(CrudBase[models.Price, schemas.PriceCreate, schemas.PriceCreate]):
    def get_many(self,
                 db: Session,
                 device_name: str,
                 newer_than: Optional[datetime] = None,
                 older_than: Optional[datetime] = None) -> List[models.Price]:
        q = db.query(models.Price).filter(models.Price.device_name == device_name)

        if newer_than is not None:
            q = q.filter(models.Price.date > newer_than)

        if older_than is not None:
            q = q.filter(models.Price.date < older_than)

        devices = q.all()

        logging.debug(f"Got list of prices for device {device_name}")

        return devices

    def create_many(self,
                    db: Session,
                    name: str,
                    prices: List[schemas.PriceCreate]) -> List[models.Price]:
        db_prices = [self.t_model(**price.dict(),
                                  device_name=name) for price in prices]
        db.add_all(db_prices)
        db.commit()
        [db.refresh(db_price) for db_price in db_prices]

        return db_prices


price = CrudPrices(models.Price)
