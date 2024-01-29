from fastapi import FastAPI

app = FastAPI()

#Users

@app.get("/users")
def GetUsers():
    return "TODO: Get Users"

@app.post("/users")
def PostUsers():
    return "TODO: Add Users"

@app.get("/users/{user_id}")
def GetUser():
    return "TODO: Retrieve a specific user"

@app.get("/users/{user_id}/chats")
def GetUserChats():
    return "TODO Retrieve the chats from a specific user"


#Chats


@app.get("/chats")
def GetChats():
    return "TODO: Get chats"

@app.get("/chats/{chat_id}")
def GetChat():
    return "TODO: Get chat"

@app.put("/chats/{chat_id}")
def PutChat():
    return "TODO: Update chat"

@app.delete("/chats/{chat_id}")
def DeleteChat():
    return "TODO: Delete chat"

@app.get("/chats/{chat_id}/messages")
def GetChatMessages():
    return "TODO: Get chat messages"

@app.get("/chats/{chat_id}/users")
def GetChatUsers():
    return "TODO: Get chat users"