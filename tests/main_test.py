import backend.main
from fastapi.testclient import TestClient
from backend.main import app

test_client = TestClient(app)

#User Tests

def test_GetUsers():
    response = test_client.get("/users")
    assert response.status_code == 200

def test_PostUsers():
    return "TODO: Add Users"

def test_GetUser():
    return "TODO: Retrieve a specific user"

def test_GetUserChats():
    return "TODO Retrieve the chats from a specific user"


#Chat Tests

def test_GetChats():
    return "TODO: Get chats"

def test_GetChat():
    return "TODO: Get chat"

def test_PutChat():
    return "TODO: Update chat"

def test_DeleteChat():
    return "TODO: Delete chat"

def test_GetChatMessages():
    return "TODO: Get chat messages"

def test_GetChatUsers():
    return "TODO: Get chat users"