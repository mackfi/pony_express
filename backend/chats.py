from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

class Chat(BaseModel):
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

@chats_router.get("/", description="Retreives all chats from the DB.", name="Get Chats")
def GetChats():
    return "TODO: Get chats"

@chats_router.get("/{chat_id}", description="Retreives the specified chat from the DB.", name="Get Chat")
def GetChat():
    return "TODO: Get chat"

@chats_router.put("/{chat_id}", description="Updates the specified chat in the DB.", name="Put Chat")
def PutChat():
    return "TODO: Update chat"

@chats_router.delete("/{chat_id}", description="Deletes the specified chat from the DB.", name="Delete Chat")
def DeleteChat():
    return "TODO: Delete chat"

@chats_router.get("/{chat_id}/messages", description="Retreives all messages associated with the specified chat.", name="Get Chat Messages")
def GetChatMessages():
    return "TODO: Get chat messages"

@chats_router.get("/{chat_id}/users", description="Retreieves all users associated with the specified chat.", name="Get Chat Users")
def GetChatUsers():
    return "TODO: Get chat users"