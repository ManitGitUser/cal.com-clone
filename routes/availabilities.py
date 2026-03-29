from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import services
import schemas
from database import get_db

router = APIRouter(prefix="/availabilities", tags=["availabilities"])

@router.post("/", response_model=schemas.Availability)
def create_availability(availability: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    return services.create_availability(db=db, availability=availability)

@router.get("/", response_model=List[schemas.Availability])
def read_availabilities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    availabilities = services.get_availabilities(db, skip=skip, limit=limit)
    return availabilities

@router.delete("/{availability_id}", response_model=schemas.Availability)
def delete_availability(availability_id: int, db: Session = Depends(get_db)):
    db_availability = services.delete_availability(db, availability_id=availability_id)
    if db_availability is None:
        raise HTTPException(status_code=404, detail="Availability not found")
    return db_availability
