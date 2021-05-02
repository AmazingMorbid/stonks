from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional, List

from fastapi import Depends
from requests import Session
from starlette.responses import JSONResponse

from stonks_types import schemas

# from stonks_api.api.v1.endpoints.device_recognizer import device_recognizer
from stonks_api.api.v1.endpoints.devices import device_not_found
from stonks_api.crud import crud_offers, crud_delivery, crud_devices
from stonks_api.database import get_db

router = APIRouter()


def offer_not_found(offer):
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")


def delivery_not_found(delivery):
    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")


@router.get("/", response_model=List[schemas.Offer])
def get_offers(skip: int = 0,
               limit: int = 50,
               newer_than: Optional[datetime] = None,
               older_than: Optional[datetime] = None,
               db: Session = Depends(get_db)):
    if (newer_than is not None and older_than is not None) and newer_than > older_than:
        raise HTTPException(status_code=422, detail={"error": "newer_than cannot be greater than older than, as it "
                                                              "will always return no offers."})
    offers = crud_offers.get_offers(db,
                                    skip=skip,
                                    limit=limit,
                                    newer_than=newer_than,
                                    older_than=older_than)

    return offers


@router.get("/{offer_id}", response_model=schemas.Offer)
def get_offer(offer_id: str, db: Session = Depends(get_db)):
    offer = crud_offers.get_offer(db, offer_id=offer_id)

    offer_not_found(offer)

    return offer


@router.post("/", response_model=schemas.Offer, status_code=201)
def create_offer(offer: schemas.OfferCreate,
                 get_device_model: bool = False,
                 db: Session = Depends(get_db)):
    db_offer = crud_offers.get_offer(db, offer.id)

    if db_offer is not None:
        raise HTTPException(status_code=409, detail="Offer already exists. Consider using upsert route.")

    # if get_device_model is True get device model and set it
    # if get_device_model:
    #     model = device_recognizer.get_info(offer.title).model.lower()
    #     offer.device_model = model if len(model) > 2 else None

    if offer.device is not None:
        device = crud_devices.get_one_by_name(db=db,
                                              device_name=offer.device)

        device_not_found(device)

    db_offer = crud_offers.create_offer(db, offer)

    return db_offer


@router.put("/{offer_id}", response_model=schemas.Offer)
def update_offer(offer_id: str,
                 offer: schemas.OfferUpdate,
                 get_device_model: bool = False,
                 db: Session = Depends(get_db)):
    """
    Update offer information.
    Note that you cannot update delivery information from here, instead you must call /offers/id/deliveries/id
    """
    db_offer = crud_offers.get_offer(db, offer_id)

    offer_not_found(db_offer)

    # if get_device_model is True get device model and set it
    # if get_device_model:
    #     model = device_recognizer.get_info(offer.title).model.lower()
    #     offer.device_model = model if len(model) > 2 else None

    db_offer = crud_offers.update_offer(db, offer_id, offer)

    return db_offer


@router.delete("/{offer_id}")
def delete_offer(offer_id: str, db: Session = Depends(get_db)):
    db_offer = crud_offers.get_offer(db, offer_id)
    offer_not_found(db_offer)

    crud_offers.delete_offer(db, offer_id)

    return JSONResponse({"detail": "Offer has been deleted"})


@router.get("/{offer_id}/deliveries", response_model=List[schemas.Delivery])
def get_deliveries_for_offer(offer_id: str,
                             skip: int = 0,
                             limit: int = 50,
                             db: Session = Depends(get_db)):
    offer = crud_offers.get_offer(db=db, offer_id=offer_id)
    offer_not_found(offer)

    deliveries = crud_delivery.get_deliveries_for_offer(db=db,
                                                        offer_id=offer_id,
                                                        skip=skip,
                                                        limit=limit)

    return deliveries


@router.post("/{offer_id}/deliveries", response_model=List[schemas.Delivery], status_code=201)
def add_deliveries_for_offer(offer_id: str,
                             deliveries: List[schemas.DeliveryCreate],
                             db: Session = Depends(get_db)):
    offer = crud_offers.get_offer(db=db, offer_id=offer_id)
    offer_not_found(offer)

    db_deliveries = crud_delivery.create_deliveries_for_offer(db=db,
                                                              offer_id=offer_id,
                                                              deliveries=deliveries)

    return db_deliveries


@router.delete("/{offer_id}/deliveries")
def delete_deliveries_for_offer(offer_id: str,
                                db: Session = Depends(get_db)):
    offer = crud_offers.get_offer(db=db, offer_id=offer_id)
    offer_not_found(offer)

    crud_delivery.delete_deliveries_for_offer(db=db,
                                              offer_id=offer_id)

    return {"message": f"Deliveries for offer {offer_id} had been deleted."}


@router.put("/{offer_id}/deliveries/{delivery_id}", response_model=schemas.Delivery)
def update_delivery(offer_id: str,
                    delivery_id: int,
                    delivery: schemas.DeliveryUpdate,
                    db: Session = Depends(get_db)):
    offer = crud_offers.get_offer(db=db,
                                  offer_id=offer_id)
    offer_not_found(offer)

    db_delivery = crud_delivery.get_delivery(db=db,
                                             delivery_id=delivery_id)
    delivery_not_found(db_delivery)

    db_delivery = crud_delivery.update_delivery(db=db,
                                                delivery_id=delivery_id,
                                                delivery=delivery)

    return db_delivery
