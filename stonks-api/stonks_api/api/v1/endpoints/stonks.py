from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from stonks_types import schemas
from stonks_api.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Stonks])
def get_stonks_list(skip: int = 0,
                    limit: int = 50,
                    sort: schemas.StonksSortBy = schemas.StonksSortBy.stonks_amount_desc,
                    db: Session = Depends(get_db)):
    pass


@router.get("/{stonks_id}", response_model=schemas.Stonks)
def get_stonks(stonks_id: int,
               db: Session = Depends(get_db)):
    pass


@router.post("/", response_model=schemas.Stonks)
def create_stonks(stonks: schemas.Stonks,
                  db: Session = Depends(get_db)):
    pass


@router.put("/{stonks_id}")
def update_stonks(stonks_id: int,
                  stonks: schemas.Stonks,
                  db: Session = Depends(get_db)):
    pass


@router.delete("/{stonks_id}")
def delete_stonks(stonks_id: int,
                  db: Session = Depends(get_db)):
    pass
