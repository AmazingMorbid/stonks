from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import crud
from stonks_api.api.v1.endpoints.devices import device_not_found
from stonks_api.database import get_db

router = APIRouter()


@router.get("/{device_name}", response_model=schemas.Prices)
def get_prices_for_device(device_name: str,
                          newer_than: Optional[datetime] = None,
                          older_than: Optional[datetime] = None,
                          db: Session = Depends(get_db)):
    device = crud.device.get_one_by_name(db=db, name=device_name)
    device_not_found(device)

    db_prices = crud.price.get_many(db=db,
                                    device_name=device_name,
                                    newer_than=newer_than,
                                    older_than=older_than)

    return schemas.Prices(prices=db_prices)


@router.post("/{device_name}", response_model=schemas.Prices, status_code=201)
def create_prices(device_name: str,
                  prices: schemas.PricesCreate,
                  db: Session = Depends(get_db)):
    device = crud.device.get_one_by_name(db=db, name=device_name)
    device_not_found(device)
    db_prices = crud.price.create_many(db=db,
                                       name=device_name,
                                       prices=prices.prices)
    device.last_price_update = datetime.utcnow()
    db.commit()

    return schemas.Prices(prices=db_prices)
