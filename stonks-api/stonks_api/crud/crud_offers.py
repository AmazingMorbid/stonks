import logging
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from stonks_types import schemas

from stonks_api import models
from stonks_api.crud import crud_delivery, crud_devices

LOG_TAG = "crud_offers"


def _log(level, msg):
    logging.log(level, f"[{LOG_TAG}]: {msg}")


def get_offer(db: Session, offer_id: str) -> Optional[models.Offer]:
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()

    logging.info(f"[{LOG_TAG}]: Got offer: {offer}")

    return offer


def get_offers(db: Session,
               skip: int,
               limit: int,
               newer_than: Optional[datetime] = None,
               older_than: Optional[datetime] = None,
               last_stonks_check_before: Optional[datetime] = None,
               has_device: Optional[bool] = None) -> List[models.Offer]:
    q = db.query(models.Offer)

    if has_device is not None:
        if has_device:
            q = q.filter(models.Offer.device_name != None)
        else:
            q = q.filter(models.Offer.device_name == None)

    if last_stonks_check_before is not None:
        q = q.filter((models.Offer.last_stonks_check < last_stonks_check_before) |
                     (models.Offer.last_stonks_check == None))

    if newer_than is not None:
        q = q.filter(models.Offer.last_scraped_time > newer_than)

    if older_than is not None:
        q = q.filter(models.Offer.last_scraped_time < older_than)

    q = q.offset(skip).limit(limit)

    offers = q.all()

    _log(logging.INFO, "Got list of offers.")

    return offers


def create_offer(db: Session, offer: schemas.OfferCreate) -> models.Offer:
    # Remove deliveries from dictionary, cause it not compatible with sqlalchemy :<
    dict_offer = offer.dict()
    dict_offer.pop("deliveries")
    dict_offer.pop("device_name")

    db_offer = models.Offer(**dict_offer)
    db.add(db_offer)
    db.flush()
    db.refresh(db_offer)

    if offer.deliveries is not None:
        crud_delivery.create_deliveries_for_offer(db=db,
                                                  offer_id=offer.id,
                                                  deliveries=offer.deliveries)

    # if offer.device is not None:
    if offer.device_name is not None:
        db_offer.device = crud_devices.get_one_by_name(db=db,
                                                       device_name=offer.device_name)

    db.commit()

    return db_offer


def update_offer(db: Session, offer_id: str, offer: schemas.OfferUpdate):
    query = db.query(models.Offer).filter(models.Offer.id == offer_id)

    query.update(offer.dict())
    db.commit()

    db_offer = query.first()

    _log(logging.INFO, f"Updated offer with id {offer_id}")

    return db_offer


def delete_offer(db: Session, offer_id: str):
    db.query(models.Offer).filter_by(id=offer_id).delete()
    db.commit()

    _log(logging.INFO, f"Deleted offer with id {offer_id}")
