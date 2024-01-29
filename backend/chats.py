from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/chats", tags=["Chats"])

class Chat(BaseModel):
    id: str
    name: str
    user_ids: []
    owner_id: str
    created_at: datetime