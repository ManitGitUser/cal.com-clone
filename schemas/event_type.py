from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EventTypeBase(BaseModel):
    title: str
    slug: str
    duration: int = Field(..., gt=0, description="Duration in minutes, must be positive")

class EventTypeCreate(EventTypeBase):
    pass

class EventType(EventTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
