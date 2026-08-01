from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VehicleBase(BaseModel):
    company: str
    model: str
    year: int
    vehicle_type: str
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    vin: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class InspectionImageResponse(BaseModel):
    id: int
    angle: str
    file_path: str

    class Config:
        from_attributes = True

class InspectionResponse(BaseModel):
    id: int
    vehicle_id: int
    status: str
    created_at: datetime
    images: List[InspectionImageResponse] = []

    class Config:
        from_attributes = True
