from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vehicle import Inspection
from app.models.damage import DamageRecord
from app.models.cost import CostEstimate
from app.models.chat import ChatMessage
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.services.llm_engine import get_ai_response

router = APIRouter()

@router.get("/{inspection_id}/chat", response_model=List[ChatMessageResponse])
async def get_chat_history(
    inspection_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(ChatMessage).where(ChatMessage.inspection_id == inspection_id).order_by(ChatMessage.created_at.asc()))
    return result.scalars().all()

@router.post("/{inspection_id}/chat", response_model=ChatMessageResponse)
async def send_chat_message(
    inspection_id: int,
    payload: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verify inspection
    i_result = await db.execute(select(Inspection).where(Inspection.id == inspection_id))
    inspection = i_result.scalars().first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
        
    # 2. Save user message
    user_msg = ChatMessage(inspection_id=inspection_id, sender="user", message=payload.message)
    db.add(user_msg)
    await db.commit()
    
    # 3. Gather context for LLM
    d_result = await db.execute(select(DamageRecord).where(DamageRecord.inspection_id == inspection_id))
    damages = d_result.scalars().all()
    
    c_result = await db.execute(select(CostEstimate).where(CostEstimate.inspection_id == inspection_id))
    cost = c_result.scalars().first()
    
    h_result = await db.execute(select(ChatMessage).where(ChatMessage.inspection_id == inspection_id).order_by(ChatMessage.created_at.desc()).limit(6))
    history = h_result.scalars().all()
    # Reverse to get chronological order of the last few messages, excluding the one we just saved
    history = history[::-1][:-1] 
    
    context = {
        "damages": damages,
        "cost": cost,
        "history": history
    }
    
    # 4. Get AI Response
    ai_text = await get_ai_response(payload.message, context)
    
    # 5. Save AI message
    ai_msg = ChatMessage(inspection_id=inspection_id, sender="ai", message=ai_text)
    db.add(ai_msg)
    await db.commit()
    await db.refresh(ai_msg)
    
    return ai_msg
