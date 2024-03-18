from passlib.context import CryptContext
from sqlmodel import SQLModel, Session
from fastapi.security import OAuth2PasswordBearer 
from fastapi import APIRouter, Depends
from typing import Annotated

from backend import database as db

from backend.schema import UserInDB, User, UserResponse
from backend.database import DuplicateEntityException

import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_key = os.environ.get("JWT_KEY", default="any string you want for a dev JWT key")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegistration(SQLModel):
    """Request model to register new user."""

    username: str
    email: str
    password: str


@auth_router.post("/registration")
def register_new_user(registration: UserRegistration, session: Annotated[Session, Depends(db.get_session)]) -> UserResponse:
    hashed_password = pwd_context.hash(registration.password)
    user = UserInDB(
        **registration.model_dump(),
        hashed_password=hashed_password,
    )
    other_usernames = session.get(UserInDB, user.username)
    other_emails = session.get(UserInDB, user.email)
    
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except:
        if other_emails:
            raise DuplicateEntityException(entity_name="User", entity_field="email", entity_value=user.email)
        if other_usernames:
            raise DuplicateEntityException(entity_name="User", entity_field="username", entity_value=user.username)
    


    return UserResponse(user=user)