from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from fastapi import HTTPException
import models
import schemas

def get_event_type(db: Session, event_type_id: int):
    return db.query(models.EventType).filter(models.EventType.id == event_type_id).first()

def get_event_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EventType).offset(skip).limit(limit).all()

def create_event_type(db: Session, event_type: schemas.EventTypeCreate):
    db_event_type = models.EventType(
        title=event_type.title,
        description=event_type.description,
        duration=event_type.duration,
        slug=event_type.slug
    )
    db.add(db_event_type)
    db.commit()
    db.refresh(db_event_type)
    return db_event_type

def delete_event_type(db: Session, event_type_id: int):
    db_event_type = get_event_type(db, event_type_id)
    if db_event_type:
        db.delete(db_event_type)
        db.commit()
    return db_event_type

def get_available_slots(db: Session, event_type_id: int, target_date: date):
    event_type = get_event_type(db, event_type_id)
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")

    from datetime import timezone

    try:
        start_of_day = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_of_day = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=timezone.utc)
    except Exception:
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())

    availabilities = db.query(models.Availability).filter(
        models.Availability.event_type_id == event_type_id,
        models.Availability.start_time >= start_of_day,
        models.Availability.start_time <= end_of_day
    ).all()

    existing_bookings = db.query(models.Booking).filter(
        models.Booking.event_type_id == event_type_id,
        models.Booking.start_time >= start_of_day,
        models.Booking.start_time <= end_of_day
    ).all()
    
    booked_start_times = {booking.start_time for booking in existing_bookings}

    slot_duration = timedelta(minutes=event_type.duration)
    available_slots = []
    
    now_utc = datetime.now(timezone.utc)

    for availability in availabilities:
        current_time = availability.start_time
        while current_time + slot_duration <= availability.end_time:
            slot_end = current_time + slot_duration
            
            # Check overlap logic mapping
            # (SlotStart < BookEnd) AND (SlotEnd > BookStart)
            is_overlapping = any(
                current_time < booking.end_time and slot_end > booking.start_time
                for booking in existing_bookings
            )
            
            if not is_overlapping and current_time >= now_utc:
                available_slots.append(schemas.Slot(start_time=current_time, end_time=slot_end))
                
            current_time += slot_duration

    return available_slots
