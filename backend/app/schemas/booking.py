from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GarageBase(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    rating: Optional[float] = 0.0
    phone: Optional[str] = None

class GarageResponse(GarageBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    garage_id: int
    inspection_id: Optional[int] = None
    appointment_time: datetime

class BookingResponse(BaseModel):
    id: int
    user_id: int
    garage_id: int
    inspection_id: Optional[int]
    appointment_time: datetime
    status: str
    created_at: datetime
    
    garage: Optional[GarageResponse] = None

    class Config:
        from_attributes = True
