from pydantic import BaseModel
from typing import List, Optional

class CostEstimateBase(BaseModel):
    labor_cost_min: float
    labor_cost_max: float
    parts_cost_min: float
    parts_cost_max: float
    paint_cost_min: float
    paint_cost_max: float
    total_cost_min: float
    total_cost_max: float

class CostEstimateResponse(CostEstimateBase):
    id: int
    inspection_id: int

    class Config:
        from_attributes = True
