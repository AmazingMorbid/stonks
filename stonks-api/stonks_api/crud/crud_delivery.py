from typing import List, Optional

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models


def create_deliveries_for_offer(db: Session,
                                offer_id: str,
                                deliveries: List[schemas.DeliveryCreate]) -> List[models.Delivery]:
    db_deliveries = [models.Delivery(**delivery.dict(),
                                     offer_id=offer_id) for delivery in deliveries]
    db.add_all(db_deliveries)
    db.commit()

    return db_deliveries


def get_deliveries_for_offer(db: Session,
                             offer_id: str,
                             skip: int = 0,
                             limit: int = 50) -> List[schemas.Delivery]:
    db_offers = db.query(models.Delivery).filter(models.Delivery.offer_id == offer_id).offset(skip).limit(limit).all()

    return db_offers


def get_delivery(db: Session,
                 delivery_id: int) -> Optional[models.Delivery]:
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()

    return delivery


def update_delivery(db: Session,
                    delivery_id: int,
                    delivery: schemas.DeliveryUpdate) -> models.Delivery:
    query = db.query(models.Delivery).filter(models.Delivery.id == delivery_id)

    query.update(delivery.dict())
    db.commit()

    delivery = query.first()

    return delivery


def delete_deliveries_for_offer(db: Session,
                                offer_id: str):
    db.query(models.Delivery).filter(models.Delivery.offer_id == offer_id).delete()
    db.commit()
