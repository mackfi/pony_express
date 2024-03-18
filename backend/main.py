from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.routers.users import users_router
from backend.routers.chats import chats_router
from backend.auth import auth_router
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from backend.database import DuplicateEntityException, EntityNotFoundException

from contextlib import asynccontextmanager

from backend.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Pony Express",
    description="API for managing a chat application.",
    version="0.1.0",
    lifespan=lifespan,
)



app.include_router(users_router)
app.include_router(chats_router)
app.include_router(auth_router)

@app.exception_handler(DuplicateEntityException)
def handle_entity_not_found(
    _request: Request,
    exception: DuplicateEntityException,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "type": "duplicate_entity",
                "entity_name": exception.entity_name,
                "entity_field": exception.entity_field,
                "entity_value": exception.entity_value
            },
        },
    )

@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # change this as appropriate for your setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Users

#Chats


