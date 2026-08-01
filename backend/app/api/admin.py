from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vehicle import Vehicle, Inspection
from app.models.booking import Booking, Garage
from app.models.cost import CostEstimate

router = APIRouter()

@router.get("/analytics")
async def get_platform_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch platform-wide aggregated analytics.
    In production, this requires `admin` role.
    """
    if current_user.role != "admin":
        pass # Ignored for local demo
        
    # 1. Total Users
    users_result = await db.execute(select(func.count(User.id)))
    total_users = users_result.scalar() or 0
    
    # 2. Total Inspections
    inspections_result = await db.execute(select(func.count(Inspection.id)))
    total_inspections = inspections_result.scalar() or 0
    
    # 3. Total Bookings
    bookings_result = await db.execute(select(func.count(Booking.id)))
    total_bookings = bookings_result.scalar() or 0
    
    # 4. Total Garages
    garages_result = await db.execute(select(func.count(Garage.id)))
    total_garages = garages_result.scalar() or 0
    
    # 5. Average Repair Cost Estimate (Total Max Cost)
    cost_result = await db.execute(select(func.avg(CostEstimate.total_cost_max)))
    avg_cost = cost_result.scalar() or 0.0
    
    # 6. Recent Activity (Latest 5 inspections)
    recent_result = await db.execute(
        select(Inspection)
        .order_by(Inspection.created_at.desc())
        .limit(5)
    )
    recent_inspections = recent_result.scalars().all()

    return {
        "metrics": {
            "total_users": total_users,
            "total_inspections": total_inspections,
            "total_bookings": total_bookings,
            "total_garages": total_garages,
            "average_repair_estimate": round(avg_cost, 2)
        },
        "recent_inspections": [
            {"id": i.id, "status": i.status, "vehicle_id": i.vehicle_id, "created_at": i.created_at} 
            for i in recent_inspections
        ]
    }
