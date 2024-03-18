import json
from datetime import date, datetime
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine, select


from backend.schema import (
    User,
    Chat,
    Message,
    ChatUpdate,

    UserChatLinkInDB,
    UserInDB,
    ChatInDB,
    MessageInDB
)


engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
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



def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return session.exec(select(UserInDB)).all()

def get_all_chats(session: Session) -> list[Chat]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return session.exec(select(ChatInDB)).all()

# def create_user(user_id: str) -> User:
#     """
#     Create a new user in the database.

#     :param user_ide: id of the user to be created
#     :return: the newly created user
#     """
#     if user_id in DB["users"]:

#         raise DuplicateEntityException(entity_name="User", entity_id=user_id)

#     user = User(
#         id=user_id,
#         created_at=datetime.now()
#     )
#     DB["users"][user.id] = user.model_dump()
#     return user

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


def get_chat_by_id(chat_id: str) -> Chat:
    """
    Retrieve an chat from the database.

    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    if chat_id in DB["chats"]:
        return Chat(**DB["chats"][chat_id])
    
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(session: Session, chat_id: int, update: ChatUpdate) -> Chat:
    """
    Update a chat in the database.

    :param user_id: id of the chat to be updated
    :param user_update: attributes to be updated on the chat
    :return: the updated chat
    """

    chat = session.get(ChatInDB, chat_id)
    for attr, value in update.model_dump(exclude_unset=True).items():
        setattr(chat, attr, value)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return chat

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
        return chat.messages
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_chat_users_by_id(session: Session, chat_id: int) -> list[User]:
    """
    Retrieve all users from a specified chat.

    :return: list of users.
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat.users
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_user_chats(session: Session, user_id: int) -> list[Chat]:
    """
    Retrieve all users from a specified chat.

    :return: list of users.
    """
    user = get_user_by_id(session, user_id)
    if user:
        return user.chats
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)
    
    retList = []

    return retList
