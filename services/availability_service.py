from sqlalchemy.orm import Session
import models
import schemas

def get_availabilities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Availability).offset(skip).limit(limit).all()

def create_availability(db: Session, availability: schemas.AvailabilityCreate):
    db_availability = models.Availability(**availability.model_dump())
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

def delete_availability(db: Session, availability_id: int):
    db_availability = db.query(models.Availability).filter(models.Availability.id == availability_id).first()
    if db_availability:
        db.delete(db_availability)
        db.commit()
    return db_availability
