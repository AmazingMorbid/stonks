from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from stonks_types import schemas

from stonks_api.crud import crud_devices
from stonks_api.database import get_db

router = APIRouter()


def device_not_found(device):
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found.")


@router.get("/", response_model=List[schemas.Device])
def get_devices(limit: int = 500,
                skip: int = 0,
                last_price_update_before: datetime = None,
                db: Session = Depends(get_db)):
    devices = crud_devices.get_many(db=db,
                                    limit=limit,
                                    skip=skip,
                                    last_price_update_before=last_price_update_before)

    return devices


@router.post("/", response_model=schemas.Device, status_code=201)
def create_device(device: schemas.DeviceCreate,
                  db: Session = Depends(get_db)):
    db_device = crud_devices.get_one_by_name(db=db,
                                             device_name=device.name)
    if db_device is not None:
        raise HTTPException(status_code=409,
                            detail="Device already exists.")

    db_device = crud_devices.create(db=db,
                                    device=device)

    return db_device


@router.delete("/{device_name}")
def delete_device(device_name: str,
                  db: Session = Depends(get_db)):
    db_offer = crud_devices.get_one_by_name(db=db,
                                            device_name=device_name)
    device_not_found(db_offer)

    crud_devices.delete_by_name(db=db,
                                device_name=device_name)

    return JSONResponse({"detail": "Device has been deleted."})
