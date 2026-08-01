from sqlalchemy.ext.asyncio import AsyncSession
from app.models.damage import DamageRecord
from app.models.cost import CostEstimate

def calculate_costs(damages: list[DamageRecord]) -> CostEstimate:
    """
    Mock cost engine logic. Analyzes damages and computes min/max pricing.
    """
    labor_min, labor_max = 0.0, 0.0
    parts_min, parts_max = 0.0, 0.0
    paint_min, paint_max = 0.0, 0.0
    
    for damage in damages:
        # Base multiplier by severity
        multiplier = {"Low": 1.0, "Medium": 2.0, "High": 4.0, "Critical": 6.0}.get(damage.severity, 1.0)
        
        # Labor
        labor_min += 50 * multiplier
        labor_max += 80 * multiplier
        
        # Paint (Scratches and Dents usually require paint)
        if damage.damage_type in ["Scratch", "Dent"]:
            paint_min += 100 * multiplier
            paint_max += 200 * multiplier
            
        # Parts (Replace vs Repair)
        if damage.repairability == "Replace":
            parts_min += 200 * multiplier
            parts_max += 400 * multiplier
        else:
            parts_min += 20 * multiplier
            parts_max += 50 * multiplier

    return CostEstimate(
        labor_cost_min=labor_min,
        labor_cost_max=labor_max,
        parts_cost_min=parts_min,
        parts_cost_max=parts_max,
        paint_cost_min=paint_min,
        paint_cost_max=paint_max,
        total_cost_min=labor_min + parts_min + paint_min,
        total_cost_max=labor_max + parts_max + paint_max
    )

async def generate_cost_estimate(inspection_id: int, db: AsyncSession):
    # Fetch damages
    from sqlalchemy.future import select
    result = await db.execute(select(DamageRecord).where(DamageRecord.inspection_id == inspection_id))
    damages = result.scalars().all()
    
    cost_estimate = calculate_costs(damages)
    cost_estimate.inspection_id = inspection_id
    
    db.add(cost_estimate)
    await db.commit()
    await db.refresh(cost_estimate)
    return cost_estimate
