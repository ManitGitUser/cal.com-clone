from pydantic import BaseModel
from datetime import datetime

class Slot(BaseModel):
    start_time: datetime
    end_time: datetime
