from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import services
import schemas
from database import get_db
from datetime import date

router = APIRouter(prefix="/event-types", tags=["event_types"])

@router.post("/", response_model=schemas.EventType)
def create_event_type(event_type: schemas.EventTypeCreate, db: Session = Depends(get_db)):
    return services.create_event_type(db=db, event_type=event_type)

@router.get("/", response_model=List[schemas.EventType])
def read_event_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    event_types = services.get_event_types(db, skip=skip, limit=limit)
    return event_types

@router.get("/{event_type_id}", response_model=schemas.EventType)
def read_event_type(event_type_id: int, db: Session = Depends(get_db)):
    db_event_type = services.get_event_type(db, event_type_id=event_type_id)
    if db_event_type is None:
        raise HTTPException(status_code=404, detail="Event type not found")
    return db_event_type

@router.delete("/{event_type_id}", response_model=schemas.EventType)
def delete_event_type(event_type_id: int, db: Session = Depends(get_db)):
    db_event_type = services.delete_event_type(db, event_type_id=event_type_id)
    if db_event_type is None:
        raise HTTPException(status_code=404, detail="Event type not found")
    return db_event_type

@router.get("/{event_type_id}/slots", response_model=List[schemas.Slot])
def get_available_slots(event_type_id: int, target_date: date, db: Session = Depends(get_db)):
    return services.get_available_slots(db, event_type_id=event_type_id, target_date=target_date)
