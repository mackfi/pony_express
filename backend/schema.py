from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from datetime import datetime
import json

class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)


class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )


class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")


class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")


#
#   OLD MODELS
#
class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    user: User

class Chat(BaseModel):
    id: int
    name: str
    owner: User
    created_at: datetime

class ChatUpdate(SQLModel):
    name: str

class ChatMetaData(BaseModel):
    message_count: int
    user_count: int


class UserUpdate(SQLModel):
    username: str = None
    email: str = None

class Message(BaseModel):
    id: int
    text: str
    chat_id: int
    user: User
    created_at: datetime

class ChatResponse(BaseModel):
    meta: ChatMetaData
    chat: Chat
    messages: list[Message] = None
    users: list[User] = None

class MessageResponse(BaseModel):
    message: Message

class MessageCreate(BaseModel):
    text: str

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[User]

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""

    meta: Metadata
    chats: list[Chat]

class MessageCollection(BaseModel):
    """Represents an API response for a collection of messages."""

    meta: Metadata
    messages: list[Message]