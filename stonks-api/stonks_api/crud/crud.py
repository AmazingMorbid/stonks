from typing import TypeVar, Generic, List, Optional, Type, Callable, Union

from loguru import logger
from sqlalchemy.orm import Session

TModel = TypeVar("TModel")
CreateType = TypeVar("CreateType")
UpdateType = TypeVar("UpdateType")


class CrudBase(Generic[TModel, CreateType, UpdateType]):
    def __init__(self, t_model: Type[TModel]):
        self.t_model = t_model

    def get_one(self, db: Session, id: Union[int, str]) -> Optional[TModel]:
        return db.query(TModel).filter(TModel.id == id).first()

    def get_many(self,
                 db: Session,
                 skip: int,
                 limit: int, ) -> List[TModel]:
        logger.debug(f"Getting many models of {self.t_model}")
        return db.query(self.t_model).offset(skip).limit(limit).all()

    def create(self,
               db: Session,
               new_model: Union[Type[CreateType], dict]) -> TModel:
        logger.debug(f"Creating model {new_model}")

        # Support for both plain dictionaries and pydantic models
        if type(new_model) == dict:
            db_model = self.t_model(**new_model)
        else:
            db_model = self.t_model(**new_model.dict())

        db.add(db_model)
        db.commit()
        db.refresh(db_model)

        return db_model

    def update(self,
               db: Session,
               update_model: Type[UpdateType]) -> TModel:
        pass

    def remove(self,
               db: Session,
               id: int):
        pass


# class CrudOffer(CrudBase):
#     pass


# class CrudPrice(CrudBase):
#     pass
