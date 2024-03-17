import json
from datetime import date, datetime
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine, select


from backend.schema import (
    User,
    Chat,
    Message,

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
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id



def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return session.exec(select(UserInDB)).all()

def get_all_chats() -> list[Chat]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return [Chat(**chat_data) for chat_data in DB["chats"].values()]

def create_user(user_id: str) -> User:
    """
    Create a new user in the database.

    :param user_ide: id of the user to be created
    :return: the newly created user
    """
    if user_id in DB["users"]:

        raise DuplicateEntityException(entity_name="User", entity_id=user_id)

    user = User(
        id=user_id,
        created_at=datetime.now()
    )
    DB["users"][user.id] = user.model_dump()
    return user

def get_user_by_id(user_id: str) -> User:
    """
    Retrieve an user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    if user_id in DB["users"]:
        return User(**DB["users"][user_id])
    
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

def update_chat(chat_id: str, name: str) -> Chat:
    """
    Update a chat in the database.

    :param user_id: id of the chat to be updated
    :param user_update: attributes to be updated on the chat
    :return: the updated chat
    """

    chat = get_chat_by_id(chat_id)
    setattr(chat, "name", name)
    DB["chats"][chat.id] = chat.model_dump()
    return chat

def delete_chat(chat_id: str):
    """
    Delete an animal from the database.

    :param animal_id: the id of the animal to be deleted
    :raises EntityNotFoundException: if no such animal exists
    """

    chat = get_chat_by_id(chat_id)
    del DB["chats"][chat.id]

def get_chat_messages_by_id(chat_id: str) -> list[Message]:
    """
    Retrieve all messages from a specified chat.

    :return: list of messages.
    """
    get_chat_by_id(chat_id)
    return [Message(**message_data) for message_data in DB["chats"][chat_id]["messages"]]

def get_chat_users_by_id(chat_id: str) -> list[User]:
    """
    Retrieve all users from a specified chat.

    :return: list of users.
    """
    get_chat_by_id(chat_id)
    user_ids = DB["chats"][chat_id]["user_ids"]
    user_list = []
    for id in user_ids:
        user_list.append(get_user_by_id(id))

    print(user_list)
    #TODO: Fix formatting, put messages: {} in front and remove chat info
    return user_list

def get_user_chats(user_id: str) -> list[Chat]:
    """
    Retrieve all users from a specified chat.

    :return: list of users.
    """
    get_user_by_id(user_id)
    chats = DB["chats"]
    chat_list = []
    for key, value in chats.items():
        for id in value["user_ids"]:
            if id == user_id:
                chat_list.append(key)
    
    retList = []
    for id in chat_list:
        retList.append(get_chat_by_id(id))

    return retList
