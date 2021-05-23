from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models, crud
from stonks_api.crud.crud import CrudBase


class CrudStonks(CrudBase[models.Stonks, schemas.StonksCreate, schemas.StonksUpdate]):
    def get_many(self,
                 db: Session,
                 skip: int,
                 limit: int,
                 is_active: bool = True) -> models.Stonks:
        logger.debug(f"Getting many models of {type(self.model)}")
        return db\
            .query(self.model)\
            .filter(self.model.is_active == is_active)\
            .order_by(self.model.stonks_amount.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def create_for_offer(self,
                         db: Session,
                         offer_id: str,
                         stonks: schemas.StonksCreate) -> models.Stonks:
        # Stonks dictionary without fees with offer id
        stonks_dict = {**stonks.dict(exclude={"fees"}), "offer_id": offer_id}
        db_stonks = super().create(db=db,
                                   new_model=stonks_dict)

        if stonks.fees is not None:
            crud.fees.create_many(db=db,
                                  stonks_id=db_stonks.id,
                                  fees=stonks.fees)

        crud.offer.update_stonks_check_date(db=db, id=offer_id)

        return db_stonks


stonks = CrudStonks(models.Stonks)

# def get_one(db: Session,
#             stonks_id: int) -> Optional[models.Stonks]:
#     return db.query(models.Stonks).filter(models.Stonks.id == stonks_id).first()
#
#
# def get_many(db: Session,
#              limit: int = 50,
#              skip: int = 50) -> List[models.Stonks]:
#     stonkses = db.query(models.Stonks).offset(skip).limit(limit).all()
#
#     return stonkses


# def create(db: Session,
#            offer_id: str,
#            stonks: schemas.StonksCreate) -> models.Stonks:
#     stonks_dict = stonks.dict()
#     stonks_dict.pop("fees")
#     db_stonks = models.Stonks(**stonks_dict,
#                               offer_id=offer_id)
#     db.add(db_stonks)
#     db.flush()
#     db.refresh(db_stonks)
#
#     if stonks.fees is not None:
#         crud_fees.create_fees_for_stonks(db=db,
#                                          stonks_id=db_stonks.id,
#                                          fees=stonks.fees)
#
#     return db_stonks


# def delete_one(db: Session,
#                stonks_id: int):
#     db.query(models.Stonks).filter(models.Stonks.id == stonks_id).delete()
#     db.commit()
