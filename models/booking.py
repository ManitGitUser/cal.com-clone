from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Booking(TimestampMixin, Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    event_type_id = Column(Integer, ForeignKey("event_types.id", ondelete="CASCADE"), index=True, nullable=False)
    start_time = Column(DateTime(timezone=True), index=True, nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    attendee_email = Column(String, index=True, nullable=False)

    event_type = relationship("EventType", back_populates="bookings")

    __table_args__ = (
        UniqueConstraint('event_type_id', 'start_time', name='uix_event_start_time'),
    )
