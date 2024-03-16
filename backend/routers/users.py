from fastapi import APIRouter, HTTPException, Body, Depends
from backend.entities import User, Chat, UserCollection, ChatCollection, UserCreate
from typing import Literal, Annotated
import json

from sqlmodel import Session

users_router = APIRouter(prefix="/users", tags=["Users"])

from backend import database as db

@users_router.get("/", description="Retreives all users from the DB.", name="Get Users")
def GetUsers(
    sort: Literal["id"] = "id",
    session: Session = Depends(db.get_session)
) -> UserCollection:
    
    """Get a collection of users."""

    sort_key = lambda user: getattr(user, sort)
    users = db.get_all_users()


    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

@users_router.post("/", description="Adds the specified user to the DB.", name="Post Users")
def PostUsers(user_create: UserCreate,
              session: Session = Depends(db.get_session)):
    return {"user": db.create_user(user_create.id)}

@users_router.get("/{user_id}", description="Retreives the specified user from the DB.", name="Get User")
def GetUser(user_id: str, session: Session = Depends(db.get_session)):
    return {"user": db.get_user_by_id(user_id)}

@users_router.get("/{user_id}/chats", description="Retreives all chats associated with a specified user from the DB.", name="Get User Chats")
def GetUserChats(user_id: str, sort: Literal["name"] = "name", session: Session = Depends(db.get_session)) -> ChatCollection:
    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_user_chats(user_id)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )
