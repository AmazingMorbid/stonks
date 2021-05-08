from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from stonks_types import schemas

from stonks_api import crud
from stonks_api.api.v1.endpoints.offers import offer_not_found
from stonks_api.crud import crud_stonks, crud_offers
from stonks_api.database import get_db

router = APIRouter()


def stonks_not_found(stonks):
    if stonks is None:
        raise HTTPException(status_code=404, detail="Stonks not found")


@router.get("/stonks", response_model=List[schemas.Stonks])
def get_stonks_list(skip: int = 0,
                    limit: int = 50,
                    sort: schemas.StonksSortBy = schemas.StonksSortBy.stonks_amount_desc,
                    db: Session = Depends(get_db)):
    db_stonkses = crud_stonks.get_many(db=db,
                                       skip=skip,
                                       limit=limit)

    return db_stonkses


@router.get("/stonks/{stonks_id}", response_model=schemas.Stonks)
def get_stonks(stonks_id: int,
               db: Session = Depends(get_db)):
    db_stonks = crud_stonks.get_one(db=db, stonks_id=stonks_id)
    stonks_not_found(db_stonks)

    return db_stonks


@router.post("/offers/{offer_id}/stonks", response_model=schemas.Stonks, status_code=201)
def create_stonks(offer_id: str,
                  stonks: schemas.StonksCreate,
                  db: Session = Depends(get_db)):
    offer = crud.offer.get_one(db=db, id=offer_id)
    offer_not_found(offer)

    db_stonks = crud_stonks.create(db=db,
                                   offer_id=offer_id,
                                   stonks=stonks)

    return db_stonks


# @router.put("/stonks/{stonks_id}")
# def update_stonks(stonks_id: int,
#                   stonks: schemas.Stonks,
#                   db: Session = Depends(get_db)):
#     pass


@router.delete("/stonks/{stonks_id}")
def delete_stonks(stonks_id: int,
                  db: Session = Depends(get_db)):
    stonks = crud_stonks.get_one(db=db, stonks_id=stonks_id)
    stonks_not_found(stonks)

    crud_stonks.delete_one(db=db, stonks_id=stonks_id)

    return {"detail": "Stonks has been deleted."}
