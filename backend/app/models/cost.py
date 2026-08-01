from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CostEstimate(Base):
    __tablename__ = "cost_estimates"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), unique=True)
    
    # Aggregated Costs
    labor_cost_min = Column(Float, nullable=False)
    labor_cost_max = Column(Float, nullable=False)
    parts_cost_min = Column(Float, nullable=False)
    parts_cost_max = Column(Float, nullable=False)
    paint_cost_min = Column(Float, nullable=False)
    paint_cost_max = Column(Float, nullable=False)
    
    total_cost_min = Column(Float, nullable=False)
    total_cost_max = Column(Float, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    inspection = relationship("Inspection")
