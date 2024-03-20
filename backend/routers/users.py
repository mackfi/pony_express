from fastapi import APIRouter, HTTPException, Body, Depends
from backend.schema import User, Chat, UserCollection, ChatCollection, UserCreate, UserInDB, UserResponse, UserUpdate
from backend.auth import get_current_user
from backend.database import user_in_db_to_user
from typing import Literal, Annotated
import json

from sqlmodel import Session

users_router = APIRouter(prefix="/users", tags=["Users"])

from backend import database as db

@users_router.get("/", description="Retreives all users from the DB.", name="Get Users")
def GetUsers(#sort: Literal["id"] = "id",
    session: Session = Depends(db.get_session)
) -> UserCollection:
    
    """Get a collection of users."""

    # sort_key = lambda user: getattr(user, sort)
    users = db.get_all_users(session)


    return UserCollection(
        meta={"count": len(users)},
        users= users#sorted(users, key=sort_key),
    )

@users_router.get("/me")
def GetSelf(user: UserInDB = Depends(get_current_user), session: Session = Depends(db.get_session),) -> UserResponse:
    user = db.get_user_by_id(session, user.id)
    return UserResponse(user=user_in_db_to_user(user))

@users_router.get("/{user_id}", description="Retreives the specified user from the DB.", name="Get User")
def GetUser(user_id: int, session: Session = Depends(db.get_session)) -> UserResponse:
    return UserResponse(user=User(**db.get_user_by_id(session, user_id).model_dump()))

@users_router.get("/{user_id}/chats", description="Retreives all chats associated with a specified user from the DB.", name="Get User Chats")
def GetUserChats(user_id: str, sort: Literal["name"] = "name", session: Session = Depends(db.get_session)) -> ChatCollection:
    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_user_chats(session, user_id)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )

@users_router.put("/me")
def UpdateSelf(update: UserUpdate, user: UserInDB = Depends(get_current_user), session: Session = Depends(db.get_session),) -> UserResponse:
    newUser = db.update_user(session, user.id, update)
    return UserResponse(user=user_in_db_to_user(newUser))