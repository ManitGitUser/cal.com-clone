from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AvailabilityBase(BaseModel):
    start_time: datetime
    end_time: datetime

class AvailabilityCreate(AvailabilityBase):
    event_type_id: int

class Availability(AvailabilityBase):
    id: int
    event_type_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
