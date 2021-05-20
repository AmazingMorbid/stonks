from typing import Optional, List

from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import models
from stonks_api.crud.crud import CrudBase


class CrudCategory(CrudBase[models.Category, schemas.CategoryCreate, schemas.CategoryUpdate]):
    def get_children(self, db: Session, parent_id: Optional[str] = None) -> List[models.Category]:
        return db.query(models.Category).filter(models.Category.parent_id == parent_id).all()

    def get_one_by_name(self, db: Session, name: str) -> Optional[models.Category]:
        return db.query(models.Category).filter(models.Category.name == name).first()


category = CrudCategory(models.Category)
