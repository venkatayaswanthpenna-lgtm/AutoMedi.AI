from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.cost import CostEstimateResponse
from datetime import datetime

class DamageRecordBase(BaseModel):
    part_name: str
    damage_type: str
    severity: str
    confidence_score: float
    repairability: str

class DamageRecordResponse(DamageRecordBase):
    id: int
    inspection_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class InspectionAnalysisResponse(BaseModel):
    inspection_id: int
    status: str
    damages: List[DamageRecordResponse] = []
    cost: Optional[CostEstimateResponse] = None
