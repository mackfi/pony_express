from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: str
    created_at: datetime

class Chat(BaseModel):
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

class Message(BaseModel):
    id: str
    user_id: str
    text: str
    created_at: datetime

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[User]

class ChatCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    chats: list[Chat]