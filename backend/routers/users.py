from fastapi import APIRouter, HTTPException
from backend.entities import User, Chat, UserCollection
from typing import Literal


users_router = APIRouter(prefix="/users", tags=["Users"])

from backend import database as db

@users_router.get("/", description="Retreives all users from the DB.", name="Get Users")
def GetUsers(
    sort: Literal["id"] = "id"
) -> UserCollection:
    
    """Get a collection of users."""

    sort_key = lambda user: getattr(user, sort)
    users = db.get_all_users()


    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

@users_router.post("/", description="Adds the specified user to the DB.", name="Post Users")
def PostUsers(user_id: str):
    return db.create_user(user_id)

@users_router.get("/{user_id}", description="Retreives the specified user from the DB.", name="Get User")
def GetUser(user_id: str) -> User:
    return db.get_user_by_id(user_id)

@users_router.get("/{user_id}/chats", description="Retreives all chats associated with a specified user from the DB.", name="Get User Chats")
def GetUserChats() -> list[Chat]:
    return "TODO Retrieve the chats from a specific user"
