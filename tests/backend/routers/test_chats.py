from datetime import date

import pytest

from backend import database as db
from backend.schema import *
from backend.auth import pwd_context
from passlib.context import CryptContext

@pytest.fixture
def default_chats(user_fixture):
    return [
        ChatInDB(
            id=3,
            name="nostromo",
            owner_id=1,
            owner=user_fixture(username="mack", email="mack@cool.mail")
        ),
        ChatInDB(
            id=2,
            name="slayy",
            owner_id=1,
            owner=user_fixture(username="mack", email="mack@cool.mail")
        ),
        ChatInDB(
            id=1,
            name="crimes",
            owner_id=2,
            owner=user_fixture(username="george", email="george@cool.mail")
        ),
    ]





def test_get_chat_invalid_id(client):
    chat_id = 999
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }




def test_update_chat_invalid_id(client):
    chat_id = 999
    update_params = {
        "name": "updated name"
    }
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }

# def test_get_chat(client, session, default_chats):
#     db_chat = default_chats[0]
#     session.add(db_chat)
#     session.commit()

#     chat_id = db_chat.id
#     response = client.get(f"/chats/{chat_id}")
#     assert response.status_code == 200

#     chat = response.json()["chat"]
#     expected_chat = db_chat.model_dump(mode="json")
#     for key, value in chat.items():
#         assert value == expected_chat[key]
