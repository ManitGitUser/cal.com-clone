from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class EventType(Base):
    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True, index=True)  # ⭐ MUST HAVE

    title = Column(String, nullable=False)
    description = Column(String)
    duration = Column(Integer)
    slug = Column(String, unique=True)

    availabilities = relationship("Availability", back_populates="event_type", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="event_type", cascade="all, delete-orphan")