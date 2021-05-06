from typing import TypeVar, Generic, List, Optional

from sqlalchemy.orm import Session

Model = TypeVar("Model")
SchemaCreate = TypeVar("SchemaCreate")
SchemaUpdate = TypeVar("SchemaUpdate")


class Crud(Generic[Model]):
    def get_one(self, db: Session) -> Optional[Model]:
        pass

    def get_many(self, db: Session) -> List[Model]:
        pass

    def create(self, db: Session, model: SchemaCreate) -> Model:
        pass

    def update(self, db: Session, model_id: int, model: SchemaUpdate) -> Model:
        pass

    def delete(self, db: Session, model_id: int):
        pass
