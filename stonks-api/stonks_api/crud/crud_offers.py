from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models, crud
from stonks_api.crud.crud import CrudBase


class CrudOffers(CrudBase[models.Offer, schemas.OfferCreate, schemas.OfferUpdate]):
    def get_many(self,
                 db: Session,
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

        return offers

    def create(self,
               db: Session,
               new_model: schemas.OfferCreate) -> models.Offer:
        # Exclude deliveries and device name;
        # They must be added separately below
        offer_dict = new_model.dict(exclude={"deliveries", "device_name"})

        db_offer = super().create(db=db,
                                  new_model=offer_dict)

        if new_model.deliveries is not None:
            crud.delivery.create_deliveries_for_offer(db=db,
                                                      offer_id=new_model.id,
                                                      deliveries=new_model.deliveries)

        if new_model.device_name is not None:
            db_offer.device = crud.device.get_one_by_name(db=db,
                                                          name=new_model.device_name)

        db.commit()

        return db_offer


offer = CrudOffers(models.Offer)
