import json
from datetime import date, datetime
from uuid import uuid4

from backend.entities import (
    User,
    Chat,
    Message
)

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


#   -------- animals --------   #


def get_all_users() -> list[User]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return [User(**user_data) for user_data in DB["users"].values()]

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
    #print(chats)
    chat_list = []
    for key, value in chats.items():
        for id in value["user_ids"]:
            if id == user_id:
                chat_list.append(key)
    
    retList = []
    for id in chat_list:
        retList.append(get_chat_by_id(id))

    return retList

# def create_animal(animal_create: AnimalCreate) -> AnimalInDB:
#     """
#     Create a new animal in the database.

#     :param animal_create: attributes of the animal to be created
#     :return: the newly created animal
#     """

#     animal = AnimalInDB(
#         id=uuid4().hex,
#         intake_date=date.today(),
#         **animal_create.model_dump(),
#     )
#     DB["animals"][animal.id] = animal.model_dump()
#     return animal

# def update_animal(animal_id: str, animal_update: AnimalUpdate) -> AnimalInDB:
#     """
#     Update an animal in the database.

#     :param animal_id: id of the animal to be updated
#     :param animal_update: attributes to be updated on the animal
#     :return: the updated animal
#     :raises EntityNotFoundException: if no such animal id exists
#     """

#     animal = get_animal_by_id(animal_id)
#     # option 1 -- write a line for each possible attribute
#     # name: str = None
#     # age: int = None
#     # kind: str = None
#     # fixed: bool = None
#     # vaccinated: bool = None
#     # if animal_update.name is not None:
#     #     animal.name = animal_update.name
#     # etc

#     # option 2 -- user .model_dump() method to transform
#     # animal_update from pydantic model to dict
#     # then use setattr on the animal model
#     # for attr, value in animal_update.model_dump().items():
#     #     if value is not None:
#     #         setattr(animal, attr, value)

#     # option 3 -- almost the same as option 2
#     for attr, value in animal_update.model_dump(exclude_none=True).items():
#         setattr(animal, attr, value)

#     # option 4 -- use dictionary merging to build a new animal
#     # animal = AnimalInDB(
#     #     **{
#     #         **animal.model_dump(),
#     #         **animal_update.model_dump(exclude_none=True),
#     #     },
#     # )

#     # update in database
#     DB["animals"][animal.id] = animal.model_dump()

#     return animal

# #   -------- users --------   #



# def create_user(user_create: UserCreate) -> UserInDB:
#     """
#     Create a new user in the database.

#     :param user_create: attributes of the user to be created
#     :return: the newly created user
#     """

#     user = UserInDB(
#         id=uuid4().hex,
#         intake_date=date.today(),
#         **user_create.model_dump(),
#     )
#     DB["users"][user.id] = user.model_dump()
#     return user


# def update_user(user_id: str, user_update: UserUpdate) -> UserInDB:
#     """
#     Update an user in the database.

#     :param user_id: id of the user to be updated
#     :param user_update: attributes to be updated on the user
#     :return: the updated user
#     """

#     user = get_user_by_id(user_id)
#     for key, value in user_update.update_attributes().items():
#         setattr(user, key, value)
#     return user