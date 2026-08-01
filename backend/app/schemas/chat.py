from pydantic import BaseModel
from datetime import datetime

class ChatMessageBase(BaseModel):
    message: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    inspection_id: int
    sender: str
    created_at: datetime

    class Config:
        from_attributes = True
