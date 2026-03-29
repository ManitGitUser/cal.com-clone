from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class EventType(TimestampMixin, Base):
    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    duration = Column(Integer, nullable=False)

    availabilities = relationship("Availability", back_populates="event_type", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="event_type", cascade="all, delete-orphan")
