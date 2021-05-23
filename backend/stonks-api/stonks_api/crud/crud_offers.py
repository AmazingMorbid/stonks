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
                 last_update_before: Optional[datetime] = None,
                 last_update_after: Optional[datetime] = None,
                 scraped_before: Optional[datetime] = None,
                 scraped_after: Optional[datetime] = None,
                 last_stonks_check_before: Optional[datetime] = None,
                 has_device: Optional[bool] = None,
                 is_active: bool = True,
                 ) -> List[models.Offer]:
        q = db.query(models.Offer)
        q = q.filter(models.Offer.is_active == is_active)

        if has_device:
            q = q.filter((models.Offer.device_name != None) & (models.Offer.device_name != "_no_device"))
        else:
            q = q.filter((models.Offer.device_name == None) | (models.Offer.device_name == "_no_device"))

        if scraped_before is not None:
            q = q.filter(models.Offer.scraped_at <= scraped_before)

        if scraped_after is not None:
            q = q.filter(models.Offer.scraped_at >= scraped_after)

        if last_update_before is not None:
            q = q.filter((models.Offer.last_update_at <= last_update_before) |
                         ((models.Offer.last_update_at == None) & (models.Offer.scraped_at <= last_update_before)))

        if last_update_after is not None:
            q = q.filter(models.Offer.last_update_at >= last_update_after)

        if last_stonks_check_before is not None:
            q = q.filter((models.Offer.last_stonks_check < last_stonks_check_before) |
                         (models.Offer.last_stonks_check == None))

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

    def update(self,
               db: Session,
               id: str,
               update_model: schemas.OfferUpdate) -> models.Offer:
        update_dict = {
            **update_model.dict(exclude={"device_name"}),
            # Convert to lower if not none, otherwise supply none
            "device_name": update_model.device_name.lower() if update_model.device_name is not None else None,
            "last_update_at": datetime.utcnow()
        }
        return super(CrudOffers, self).update(db=db,
                                              id=id,
                                              update_model=update_dict)

    def update_stonks_check_date(self,
                                 db: Session,
                                 id: str):
        return super().update(db=db,
                              id=id,
                              update_model={
                                  "last_stonks_check": datetime.utcnow(),
                              })


offer = CrudOffers(models.Offer)
