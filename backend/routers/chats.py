from fastapi import APIRouter, HTTPException, Depends, Query
from backend.schema import User, Chat, UserCollection, ChatCollection, MessageCollection, ChatUpdate, ChatResponse
from typing import Annotated, Literal

from sqlmodel import Session

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

from backend import database as db


@chats_router.get("/", description="Retreives all chats from the DB.", name="Get Chats")
def GetChats(
    #sort: Literal["name"] = "name",
    session: Session = Depends(db.get_session)
) -> ChatCollection:
    
    """Get a collection of chats."""

    #sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_all_chats(session)


    return ChatCollection(
        meta={"count": len(chats)},
        chats=chats#sorted(chats, key=sort_key),
    )

@chats_router.get("/{chat_id}", description="Retreives the specified chat from the DB.", name="Get Chat",response_model_exclude_none=True)
def GetChat(chat_id: int, include: Annotated[list[str] | None, Query(max_length=50)] = None, session: Session = Depends(db.get_session)) -> ChatResponse:
    return db.get_chat_by_id(session, chat_id, include)

@chats_router.put("/{chat_id}", description="Updates the specified chat in the DB.", name="Put Chat")
def PutChat(chat_id: str, chat_update: ChatUpdate, 
            session: Session = Depends(db.get_session)):
    return {"chat": db.update_chat(session, chat_id, chat_update)}

# @chats_router.delete("/{chat_id}", description="Deletes the specified chat from the DB.", name="Delete Chat", status_code=204, response_model=None)
# def DeleteChat(chat_id: str, session: Session = Depends(db.get_session)) -> None:
#     return db.delete_chat(chat_id)

@chats_router.get("/{chat_id}/messages", description="Retreives all messages associated with the specified chat.", name="Get Chat Messages")
def GetChatMessages(chat_id: int, sort: Literal["created_at"] = "created_at", session: Session = Depends(db.get_session)) -> MessageCollection:

    sort_key = lambda chat: getattr(chat, sort)
    messages = db.get_chat_messages_by_id(session, chat_id)
    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key),
    )

@chats_router.get("/{chat_id}/users", description="Retreieves all users associated with the specified chat.", name="Get Chat Users")
def GetChatUsers(chat_id: int, sort: Literal["id"] = "id", session: Session = Depends(db.get_session)) -> UserCollection:
    
    sort_key = lambda chat: getattr(chat, sort)
    users = db.get_chat_users_by_id(session, chat_id)
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )
