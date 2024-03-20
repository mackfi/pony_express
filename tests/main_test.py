import backend.main
from fastapi.testclient import TestClient
from backend.main import app
import pytest

test_client = TestClient(app)
# -----------------------
# -     OLD TESTS       -
# -----------------------

#User Tests

# def test_get_users():
#     response = test_client.get("/users")
#     assert response.status_code == 200

# def test_create_user():
#     create_params = {
#         "id": "billybob"
#     }
#     response = test_client.post("/users", json=create_params)
#     assert response.status_code == 200

# def test_create_existing_user():
#     create_params = {
#         "id": "bishop"
#     }
#     response = test_client.post("/users", json=create_params)
#     assert response.status_code == 422

# def test_get_user():
#     response = test_client.get("/users/bishop")
#     assert response.status_code == 200

# def test_nonexistent_user():
#     response = test_client.get("/users/ThisUserDoesNotExist")
#     assert response.status_code == 404

# def test_get_user_chats():
#     response = test_client.get("/users/bishop/chats")
#     assert response.status_code == 200

# def test_get_nonexistent_user_chats():
#     response = test_client.get("/users/ermmmm/chats")
#     assert response.status_code == 404


# #Chat Tests

# def test_get_chats():
#     response = test_client.get("/chats")
#     assert response.status_code == 200

# def test_get_chat():
#     response = test_client.get("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
#     assert response.status_code == 200

# def test_nonexistent_chat():
#     response = test_client.get("/chats/thisChatDoesNotExist")
#     assert response.status_code == 404

# def test_put_chat():
#     create_params = {
#         "name": "this is the new chat name btw. should probably shorten it later"
#     }
#     response = test_client.put("/chats/e0ec0881a2c645de842ca5dd0fa7985b", json=create_params)
#     assert response.status_code == 200
    
# def test_put_nonexistent_chat():
#     create_params = {
#         "name": "this is the new chat name btw. should probably shorten it later"
#     }
#     response = test_client.put("/chats/ThisChatDoesNotExist", json=create_params)
#     assert response.status_code == 404

# def test_delete_chat():
#     response = test_client.delete("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
#     assert response.status_code == 204

# def test_delete_nonexistent_chat():
#     response = test_client.delete("/chats/ThisChatDoesNotExist")
#     assert response.status_code == 404

# def test_get_chat_messages():
#     response = test_client.get("/chats/6ad56d52b138432a9bba609533015cf3/messages")
#     assert response.status_code == 200

# def test_get_nonexistent_chat_messages():
#     response = test_client.get("/chats/ThisChatDoesNotExist/messages")
#     assert response.status_code == 404

# def test_get_chat_users():
#     response = test_client.get("/chats/6ad56d52b138432a9bba609533015cf3/users")
#     assert response.status_code == 200

# def test_get_nonexistent_chat_users():
#     response = test_client.get("/chats/ThisChatDoesNotExist/users")
#     assert response.status_code == 404