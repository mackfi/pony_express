from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

class User(BaseModel):
    id: str
    created_at: datetime
