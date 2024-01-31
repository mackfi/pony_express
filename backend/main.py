from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.routers.users import users_router
from backend.routers.chats import chats_router
from pydantic import BaseModel
from datetime import datetime

from backend.database import DuplicateEntityException, EntityNotFoundException

app = FastAPI(
    title="Pony Express",
    description="API for managing a chat application.",
    version="0.1.0"
)


app.include_router(users_router)
app.include_router(chats_router)

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
                "entity_id": exception.entity_id,
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

#Users

#Chats


