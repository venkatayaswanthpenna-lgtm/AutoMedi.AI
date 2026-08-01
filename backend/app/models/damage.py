from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class DamageRecord(Base):
    __tablename__ = "damage_records"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"))
    part_name = Column(String, nullable=False) # e.g. "Front Bumper", "Left Door"
    damage_type = Column(String, nullable=False) # e.g. "Scratch", "Dent", "Broken"
    severity = Column(String, nullable=False) # "Low", "Medium", "High", "Critical"
    confidence_score = Column(Float, nullable=False) # 0.0 to 1.0
    repairability = Column(String, nullable=False) # "Repairable", "Replace"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    inspection = relationship("Inspection")
