from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from loguru import logger
from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import crud
from stonks_api.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def get_category(category_id: Optional[int] = None,
                 db: Session = Depends(get_db)):
    # if category_id is not None:
    categories = crud.category.get_children(db=db, parent_id=category_id)
    # logger.debug(category)
    # logger.debug(category.children)
    # else:
    #     category
    # if category is None:
    #     raise HTTPException(status_code=404,
    #                         detail="Category not found")

    return categories


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate,
                    db: Session = Depends(get_db)):
    db_category = crud.category.get_one_by_name(db=db, name=category.name)

    if db_category is not None and db_category.parent_id == category.parent_id:
        raise HTTPException(status_code=409,
                            detail="Category already exists")

    db_category = crud.category.create(db=db, new_model=category)

    return db_category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int,
                    new_category: schemas.CategoryUpdate,
                    db: Session = Depends(get_db)):
    db_category = crud.category.get_one(db=db, id=category_id)

    if db_category is None:
        raise HTTPException(status_code=404,
                            detail="Category not found")

    db_category = crud.category.update(db=db, id=category_id, update_model=new_category)

    return db_category
