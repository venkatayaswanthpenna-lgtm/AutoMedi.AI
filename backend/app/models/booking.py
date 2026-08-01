from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Garage(Base):
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    garage_id = Column(Integer, ForeignKey("garages.id"))
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=True)
    appointment_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="pending") # pending, confirmed, cancelled, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    garage = relationship("Garage")
    inspection = relationship("Inspection")
