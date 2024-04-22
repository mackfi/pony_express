import json
from datetime import date, datetime
from typing import Annotated
from fastapi import Query
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine, select
import os

from backend.schema import *

if os.environ.get("DB_LOCATION") == "RDS":
    username = os.environ.get("PG_USERNAME")
    password = os.environ.get("PG_PASSWORD")
    endpoint = os.environ.get("PG_ENDPOINT")
    port = os.environ.get("PG_PORT")
    db_url = f"postgresql://{username}:{password}@{endpoint}:{port}/{username}"
    echo = False
    connect_args = {}
else:
    db_url = "sqlite:///backend/pony_express.db"
    echo = True
    connect_args = {"check_same_thread": False}


engine = create_engine(
    db_url,
    echo=echo,
    connect_args=connect_args,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__(self, *, entity_name: str, entity_field: str, entity_value: str):
        self.entity_name = entity_name
        self.entity_field = entity_field
        self.entity_value = entity_value



def get_all_users(session: Session) -> list[User]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    users = session.exec(select(UserInDB)).all()
    retList = []
    for user in users:
        retList.append(user_in_db_to_user(user))
    return retList

def get_all_chats(session: Session) -> list[Chat]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    chats = session.exec(select(ChatInDB)).all()
    retList = []
    for chat in chats:
        retList.append(chat_in_db_to_chat(chat))
    return retList

def get_user_by_id(session: Session, user_id: int) -> User:
    """
    Retrieve an user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


def get_chat_by_id(session: Session, chat_id: int, include: list[str] = None) -> ChatResponse:
    """
    Retrieve an chat from the database.

    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        messages = chat.messages
        users = chat.users
        message_count = len(messages)
        user_count = len(users)
        if include:
            if "users" not in include:
                users = None
            if "messages" not in include:
                messages = None
        else: 
            messages = None
            users = None
        meta = ChatMetaData(message_count=message_count, user_count=user_count)

        if messages:
            retMessages = []
            for message in messages:
                retMessages.append(message_in_db_to_message(message))
        if users:    
            retUsers = []
            for user in users:
                retUsers.append(user_in_db_to_user(user))
        
        if messages and users:
            return ChatResponse(meta=meta, chat=chat_in_db_to_chat(chat), messages=retMessages, users=retUsers)
        if messages:
            return ChatResponse(meta=meta, chat=chat_in_db_to_chat(chat), messages=retMessages)
        if users:
            return ChatResponse(meta=meta, chat=chat_in_db_to_chat(chat), users=retUsers)
        return ChatResponse(meta=meta, chat=chat_in_db_to_chat(chat))
        # return ChatResponse(meta=meta, chat=chat)
    
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(session: Session, chat_id: int, update: ChatUpdate) -> Chat:
    """
    Update a chat in the database.

    :param user_id: id of the chat to be updated
    :param user_update: attributes to be updated on the chat
    :return: the updated chat
    """

    chat = session.get(ChatInDB, chat_id)
    if not chat:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)
    for attr, value in update.model_dump(exclude_unset=True).items():
        setattr(chat, attr, value)

    session.add(chat)
    session.commit()
    session.refresh(chat)
    user = user_in_db_to_user(chat.owner)
    return Chat(id=chat.id, name=chat.name, owner=user, created_at=chat.created_at)

def user_in_db_to_user(dbUser: UserInDB):
    return User(id=dbUser.id, username = dbUser.username, email = dbUser.email, created_at = dbUser.created_at)

def chat_in_db_to_chat(dbChat: ChatInDB):
    user = user_in_db_to_user(dbChat.owner)
    return Chat(id=dbChat.id, name=dbChat.name, owner=user, created_at=dbChat.created_at)

def message_in_db_to_message(dbMessage: MessageInDB):

    return Message(id=dbMessage.id, text=dbMessage.text, chat_id=dbMessage.chat_id, user=user_in_db_to_user(dbMessage.user), created_at=dbMessage.created_at)

def update_user(session: Session, user_id: int, update: UserUpdate) -> User:
    """
    Update a user in the database.

    :param username: id of the chat to be updated
    :param email: attributes to be updated on the chat
    :return: the updated user
    """

    user = session.get(UserInDB, user_id)
    for attr, value in update.model_dump(exclude_unset=True).items():
        setattr(user, attr, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def delete_chat(chat_id: str):
    """
    Delete an animal from the database.

    :param animal_id: the id of the animal to be deleted
    :raises EntityNotFoundException: if no such animal exists
    """

    chat = get_chat_by_id(chat_id)
    del DB["chats"][chat.id]

def get_chat_messages_by_id(session: Session, chat_id: int) -> list[Message]:
    """
    Retrieve all messages from a specified chat.

    :return: list of messages.
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        retList = []
        for message in chat.messages:
            retList.append(message_in_db_to_message(message))
        return retList
    
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_chat_users_by_id(session: Session, chat_id: int) -> list[User]:
    """
    Retrieve all users from a specified chat.

    :return: list of users.
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        retList = []
        for user in chat.users:
            retList.append(user_in_db_to_user(user))
        return retList
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_user_chats(session: Session, user_id: int) -> list[Chat]:
    """
    Retrieve all users from a specified chat.

    :return: list of users.
    """
    user = session.get(UserInDB, user_id)
    if user:
        retList = []
        for chat in user.chats:
            retList.append(chat_in_db_to_chat(chat))
        return retList
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)
    
    retList = []

    return retList

def create_message(session: Session, user: UserInDB, chat_id: int, text: str) -> Message:
    chat = session.get(ChatInDB, chat_id)
    if chat:
        message = MessageInDB(text=text, chat=chat, chat_id=chat_id, user=user, user_id=user.id)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message_in_db_to_message(message)
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)