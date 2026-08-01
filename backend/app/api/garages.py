from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.booking import Garage, Booking
from app.schemas.booking import GarageResponse, BookingCreate, BookingResponse
import math

router = APIRouter()

MOCK_GARAGES = [
    {"name": "Mike's Auto Body", "address": "123 Main St, Tech City", "latitude": 37.7749, "longitude": -122.4194, "rating": 4.8, "phone": "555-0101"},
    {"name": "Elite Collision Center", "address": "456 Market St, Tech City", "latitude": 37.7849, "longitude": -122.4094, "rating": 4.5, "phone": "555-0202"},
    {"name": "Downtown Mechanics", "address": "789 Mission St, Tech City", "latitude": 37.7649, "longitude": -122.4294, "rating": 4.2, "phone": "555-0303"},
    {"name": "QuickFix Garage", "address": "321 Howard St, Tech City", "latitude": 37.7949, "longitude": -122.3994, "rating": 4.9, "phone": "555-0404"}
]

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km using Haversine formula"""
    R = 6371 # Radius of earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@router.get("/", response_model=List[GarageResponse])
async def search_garages(
    lat: float = 37.7749, 
    lng: float = -122.4194, 
    radius_km: float = 10.0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search nearby garages. 
    If none exist in DB, we'll auto-seed mock data.
    """
    # Auto-seed mock data if empty
    count_result = await db.execute(select(func.count()).select_from(Garage))
    if count_result.scalar() == 0:
        for g in MOCK_GARAGES:
            db.add(Garage(**g))
        await db.commit()

    result = await db.execute(select(Garage).where(Garage.is_active == True))
    all_garages = result.scalars().all()
    
    # Filter by radius
    nearby = []
    for g in all_garages:
        dist = calculate_distance(lat, lng, g.latitude, g.longitude)
        if dist <= radius_km:
            nearby.append(g)
            
    return nearby

@router.post("/bookings", response_model=BookingResponse)
async def create_booking(
    payload: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    g_result = await db.execute(select(Garage).where(Garage.id == payload.garage_id))
    garage = g_result.scalars().first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
        
    booking = Booking(
        user_id=current_user.id,
        garage_id=payload.garage_id,
        inspection_id=payload.inspection_id,
        appointment_time=payload.appointment_time,
        status="pending"
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    
    # Fetch again to include relationship for response
    result = await db.execute(
        select(Booking).options(selectinload(Booking.garage)).where(Booking.id == booking.id)
    )
    return result.scalars().first()
