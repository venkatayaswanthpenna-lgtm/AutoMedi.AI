from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vehicle import Vehicle, Inspection
from app.models.damage import DamageRecord
from app.models.cost import CostEstimate
from app.services.reporting import generate_pdf_report

router = APIRouter()

@router.get("/{inspection_id}/report/pdf")
async def download_pdf_report(
    inspection_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch Inspection & Vehicle
    result = await db.execute(select(Inspection).where(Inspection.id == inspection_id))
    inspection = result.scalars().first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
        
    v_result = await db.execute(select(Vehicle).where(Vehicle.id == inspection.vehicle_id))
    vehicle = v_result.scalars().first()

    # Fetch Damages
    d_result = await db.execute(select(DamageRecord).where(DamageRecord.inspection_id == inspection_id))
    damages = d_result.scalars().all()

    # Fetch Cost
    c_result = await db.execute(select(CostEstimate).where(CostEstimate.inspection_id == inspection_id))
    cost = c_result.scalars().first()
    
    if not cost:
        raise HTTPException(status_code=400, detail="Cost estimation is not yet completed.")

    pdf_bytes = generate_pdf_report(inspection, vehicle, cost, damages)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AutoRepair_Report_{inspection_id}.pdf"
        }
    )
