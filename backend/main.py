from fastapi import FastAPI
from backend.users import users_router
from backend.chats import chats_router
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Pony Express",
    description="API for managing a chat application.",
    version="0.1.0"
)


app.include_router(users_router)
app.include_router(chats_router)

#Users

#Chats


