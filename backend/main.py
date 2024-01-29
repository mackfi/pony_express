from fastapi import FastAPI

app = FastAPI()

#Users

@app.get("/users", description="Retreives all users from the DB.", name="Get Users")
def GetUsers():
    return "TODO: Get Users"

@app.post("/users", description="Adds the specified user to the DB.", name="Post Users")
def PostUsers():
    return "TODO: Add Users"

@app.get("/users/{user_id}", description="Retreives the specified user from the DB.", name="Get User")
def GetUser():
    return "TODO: Retrieve a specific user"

@app.get("/users/{user_id}/chats", description="Retreives all chats associated with a specified user from the DB.", name="Get User Chats")
def GetUserChats():
    return "TODO Retrieve the chats from a specific user"


#Chats


@app.get("/chats", description="Retreives all chats from the DB.", name="Get Chats")
def GetChats():
    return "TODO: Get chats"

@app.get("/chats/{chat_id}", description="Retreives the specified chat from the DB.", name="Get Chat")
def GetChat():
    return "TODO: Get chat"

@app.put("/chats/{chat_id}", description="Updates the specified chat in the DB.", name="Put Chat")
def PutChat():
    return "TODO: Update chat"

@app.delete("/chats/{chat_id}", description="Deletes the specified chat from the DB.", name="Delete Chat")
def DeleteChat():
    return "TODO: Delete chat"

@app.get("/chats/{chat_id}/messages", description="Retreives all messages associated with the specified chat.", name="Get Chat Messages")
def GetChatMessages():
    return "TODO: Get chat messages"

@app.get("/chats/{chat_id}/users", description="Retreieves all users associated with the specified chat.", name="Get Chat Users")
def GetChatUsers():
    return "TODO: Get chat users"