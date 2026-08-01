from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.booking import Booking
from app.schemas.booking import BookingResponse

router = APIRouter()

@router.get("/bookings", response_model=List[BookingResponse])
async def get_mechanic_bookings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch all bookings. In a production app, this would filter by the mechanic's `garage_id`.
    Requires mechanic role.
    """
    if current_user.role not in ["mechanic", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    query = select(Booking).options(selectinload(Booking.garage)).order_by(Booking.appointment_time.asc())
    
    # Isolate data to the mechanic's specific garage
    if current_user.role == "mechanic":
        if not current_user.garage_id:
            return [] # No garage assigned yet
        query = query.where(Booking.garage_id == current_user.garage_id)
        
    result = await db.execute(query)
    return result.scalars().all()

@router.put("/bookings/{booking_id}/status")
async def update_booking_status(
    booking_id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update booking status (pending -> confirmed -> completed)
    """
    if current_user.role not in ["mechanic", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalars().first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    # Prevent unauthorized mechanic from editing another garage's booking
    if current_user.role == "mechanic" and booking.garage_id != current_user.garage_id:
        raise HTTPException(status_code=403, detail="Not authorized for this booking")
        
    # Simple state machine validation
    valid_transitions = {
        "pending": ["confirmed"],
        "confirmed": ["completed"],
        "completed": []
    }
    
    if status not in valid_transitions.get(booking.status, []):
        raise HTTPException(status_code=400, detail=f"Invalid transition from {booking.status} to {status}")
        
    booking.status = status
    await db.commit()
    await db.refresh(booking)
    
    return {"message": "Status updated successfully", "status": booking.status}
