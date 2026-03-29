from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    start_time: datetime
    end_time: datetime
    attendee_email: EmailStr

class BookingCreate(BookingBase):
    event_type_id: int

class Booking(BookingBase):
    id: int
    event_type_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
