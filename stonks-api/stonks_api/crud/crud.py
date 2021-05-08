from typing import TypeVar, Generic, List, Optional, Type, Union

from loguru import logger
from sqlalchemy.orm import Session

TModel = TypeVar("TModel")
CreateType = TypeVar("CreateType")
UpdateType = TypeVar("UpdateType")


class CrudBase(Generic[TModel, CreateType, UpdateType]):
    def __init__(self, t_model: Type[TModel]):
        self.model = t_model

    def get_one(self, db: Session, id: Union[int, str]) -> Optional[TModel]:
        logger.debug(f"Downloading one from db with id={id}")
        return db.query(self.model).filter(self.model.id == id).first()

    def get_many(self,
                 db: Session,
                 skip: int,
                 limit: int, ) -> List[TModel]:
        logger.debug(f"Getting many models of {type(self.model)}")
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self,
               db: Session,
               new_model: Union[Type[CreateType], dict]) -> TModel:
        logger.debug(f"Creating model {new_model}")

        # Support for both plain dictionaries and pydantic models
        if type(new_model) == dict:
            db_model = self.model(**new_model)
        else:
            db_model = self.model(**new_model.dict())

        db.add(db_model)
        db.commit()
        db.refresh(db_model)

        return db_model

    def update(self,
               db: Session,
               id: Union[int, str],
               update_model: Union[Type[UpdateType], dict]) -> TModel:
        logger.debug(f"Updating model id={id} with {update_model}")
        query = db.query(self.model).filter(self.model.id == id)

        if type(update_model) == dict:
            update_dict = update_model
        else:
            update_dict = update_model.dict()

        query.update(update_dict)
        db.commit()

        db_offer = query.first()

        return db_offer

    def remove(self,
               db: Session,
               id: int):
        logger.debug(f"Removing model id={id}")
        db.query(self.model).filter_by(id=id).delete()
        db.commit()
