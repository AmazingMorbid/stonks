import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from stonks_api import models

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://lomber:root@localhost:5432/stonks")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def create_no_device():
    _session: Session = SessionLocal()
    _no_device = _session.query(models.Device).filter(models.Device.name == "_no_device").first()

    if _no_device is None:
        _no_device = models.Device(name="_no_device")
        _session.add(_no_device)
        _session.commit()
