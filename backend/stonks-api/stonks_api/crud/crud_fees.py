from typing import List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models
from stonks_api.crud.crud import CrudBase


class CrudFees(CrudBase[models.Fee, schemas.FeeCreate, schemas.FeeUpdate]):
    def create_many(self,
                    db: Session,
                    stonks_id: int,
                    fees: List[schemas.FeeCreate]):
        db_fees = []

        for fee in fees:
            db_fee = self.model(**fee.dict(),
                                stonks_id=stonks_id)
            db.add(db_fee)
            db.flush()
            db.refresh(db_fee)
            db_fees.append(db_fee)

        db.commit()

        return db_fees


fees = CrudFees(models.Fee)

# def create_fees_for_stonks(db: Session,
#                            stonks_id: int,
#                            fees: List[schemas.FeeCreate]):
#     db_fees = [models.Fee(**fee.dict(),
#                           stonks_id=stonks_id) for fee in fees]
#     db.add_all(db_fees)
#     db.commit()
#
#     return db_fees
