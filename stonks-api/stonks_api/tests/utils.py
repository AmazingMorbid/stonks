from sqlalchemy.orm import Session

from stonks_api import models
from stonks_api.database import SessionLocal


def delete_stonks():
    db: Session = SessionLocal()
    db.query(models.Stonks).delete()
    db.commit()
    db.close()


def delete_offers():
    db: Session = SessionLocal()
    db.query(models.Offer).delete()
    db.commit()
    db.close()


def delete_devices():
    db: Session = SessionLocal()
    db.query(models.Device).delete()
    db.commit()
    db.close()


def delete_data():
    delete_stonks()
    delete_offers()
    delete_devices()
