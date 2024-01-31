from fastapi import APIRouter, HTTPException
from backend.entities import User, Chat, ChatCollection
from typing import Literal

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

from backend import database as db


@chats_router.get("/", description="Retreives all chats from the DB.", name="Get Chats")
def GetUsers(
    sort: Literal["name"] = "name"
) -> ChatCollection:
    
    """Get a collection of users."""

    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_all_chats()


    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )

@chats_router.get("/{chat_id}", description="Retreives the specified chat from the DB.", name="Get Chat")
def GetChat(chat_id: str) -> Chat:
    return db.get_chat_by_id(chat_id)

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
def GetChatUsers() -> list[User]:
    return "TODO: Get chat users"
