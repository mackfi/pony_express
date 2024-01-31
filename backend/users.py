from fastapi import APIRouter, HTTPException
from backend.entities import User, Chat


users_router = APIRouter(prefix="/users", tags=["Users"])



@users_router.get("/", description="Retreives all users from the DB.", name="Get Users")
def GetUsers() -> list[User]:
    return "TODO: Get Users"

@users_router.post("/", description="Adds the specified user to the DB.", name="Post Users")
def PostUsers():
    return "TODO: Add Users"

@users_router.get("/{user_id}", description="Retreives the specified user from the DB.", name="Get User")
def GetUser() -> User:
    return "TODO: Retrieve a specific user"

@users_router.get("/{user_id}/chats", description="Retreives all chats associated with a specified user from the DB.", name="Get User Chats")
def GetUserChats() -> list[Chat]:
    return "TODO Retrieve the chats from a specific user"

User.model_rebuild()