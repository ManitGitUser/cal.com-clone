from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
import models
import schemas

from datetime import datetime, timezone

def get_bookings(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(models.Booking)
    current_time = datetime.now(timezone.utc)
    if status == "upcoming":
        query = query.filter(models.Booking.start_time >= current_time)
    elif status == "past":
        query = query.filter(models.Booking.start_time < current_time)
    return query.offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.model_dump())
    db.add(db_booking)
    try:
        db.commit()
        db.refresh(db_booking)
        return db_booking
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Double booking is not allowed for this event at this time.")

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking
