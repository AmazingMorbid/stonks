from typing import List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models


def create_fees_for_stonks(db: Session,
                           stonks_id: int,
                           fees: List[schemas.FeeCreate]):
    db_fees = [models.Fee(**fee.dict(),
                          stonks_id=stonks_id) for fee in fees]
    db.add_all(db_fees)
    db.commit()

    return db_fees
