from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vehicle import Inspection
from app.models.damage import DamageRecord
from app.models.cost import CostEstimate
from app.schemas.damage import InspectionAnalysisResponse
from app.services.ai_engine import trigger_ai_analysis

router = APIRouter()

@router.post("/{inspection_id}/analyze")
async def analyze_inspection(
    inspection_id: int, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers the AI analysis pipeline in the background.
    """
    result = await db.execute(select(Inspection).where(Inspection.id == inspection_id))
    inspection = result.scalars().first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
        
    if inspection.status == "completed":
        return {"message": "Analysis already completed"}
        
    background_tasks.add_task(trigger_ai_analysis, inspection_id, db)
    
    return {"message": "Analysis triggered successfully. Check status later."}

@router.get("/{inspection_id}/results", response_model=InspectionAnalysisResponse)
async def get_analysis_results(
    inspection_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gets the current status and damages of an inspection.
    """
    result = await db.execute(select(Inspection).where(Inspection.id == inspection_id))
    inspection = result.scalars().first()
    
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
        
    damage_result = await db.execute(select(DamageRecord).where(DamageRecord.inspection_id == inspection_id))
    damages = damage_result.scalars().all()
    
    cost_result = await db.execute(select(CostEstimate).where(CostEstimate.inspection_id == inspection_id))
    cost = cost_result.scalars().first()
    
    return {
        "inspection_id": inspection_id,
        "status": inspection.status,
        "damages": damages,
        "cost": cost
    }
