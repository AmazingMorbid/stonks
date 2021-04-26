from typing import Optional, List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models
from stonks_api.crud import crud_fees


def get_one(db: Session,
            stonks_id: int) -> Optional[models.Stonks]:
    return db.query(models.Stonks).filter(models.Stonks.id == stonks_id).first()


def get_many(db: Session,
             limit: int = 50,
             skip: int = 50) -> List[models.Stonks]:
    stonkses = db.query(models.Stonks).offset(skip).limit(limit).all()

    return stonkses


def create(db: Session,
           offer_id: str,
           stonks: schemas.StonksCreate) -> models.Stonks:
    stonks_dict = stonks.dict()
    stonks_dict.pop("fees")
    db_stonks = models.Stonks(**stonks_dict,
                              offer_id=offer_id)
    db.add(db_stonks)
    db.flush()
    db.refresh(db_stonks)

    if stonks.fees is not None:
        crud_fees.create_fees_for_stonks(db=db,
                                         stonks_id=db_stonks.id,
                                         fees=stonks.fees)

    return db_stonks


def delete_one(db: Session,
               stonks_id: int):
    db.query(models.Stonks).filter(models.Stonks.id == stonks_id).delete()
