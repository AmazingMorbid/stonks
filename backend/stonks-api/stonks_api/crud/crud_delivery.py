from typing import List

from loguru import logger
from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models
from stonks_api.crud.crud import CrudBase


class CrudDelivery(CrudBase[models.Delivery, schemas.DeliveryCreate, schemas.DeliveryUpdate]):
    def create_deliveries_for_offer(self,
                                    db: Session,
                                    offer_id: str,
                                    deliveries: List[schemas.DeliveryCreate]) -> List[models.Delivery]:
        logger.debug(f"Creating deliveries for offer id={offer_id}")
        db_deliveries = [self.model(**delivery.dict(),
                                    offer_id=offer_id) for delivery in deliveries]
        db.add_all(db_deliveries)
        db.commit()

        return db_deliveries

    def get_deliveries_for_offer(self,
                                 db: Session,
                                 offer_id: str,
                                 skip: int = 0,
                                 limit: int = 50) -> List[schemas.Delivery]:
        logger.debug(f"Getting deliveries for offer id={offer_id}")
        db_offers = db.query(self.model).filter(self.model.offer_id == offer_id).offset(skip).limit(limit).all()

        return db_offers

    def delete_deliveries_for_offer(self,
                                    db: Session,
                                    offer_id: str):
        logger.debug(f"Deleting deliveries for offer id={offer_id}")
        db.query(self.model).filter(self.model.offer_id == offer_id).delete()
        db.commit()


delivery = CrudDelivery(models.Delivery)
