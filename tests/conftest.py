import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from backend.main import app
from backend import database as db
from backend.schema import *

import backend.auth as auth
import datetime
from datetime import *

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def logged_in_client(session, user_fixture):
    def _get_session_override():
        return session

    def _get_current_user_override():
        
        return user_fixture(username="juniper")

    app.dependency_overrides[db.get_session] = _get_session_override
    app.dependency_overrides[auth.get_current_user] = _get_current_user_override

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def user_fixture(session):
    def _build_user(
        username: str = "juniper",
        email: str = "juniper@cool.email",
        password: str = "password",
    ) -> db.UserInDB:
        return auth.register_new_user(
            auth.UserRegistration(
                username=username,
                email=email,
                password=password,
            ),
            session,
        )

    return _build_user

@pytest.fixture
def chat_fixture(session):
    def _build_chat(
        name: str ="nostromo",
        owner_id: int = 1,
        owner: UserInDB=UserInDB(username="mack", email="mack@cool.mail"),
        created_at: datetime = datetime.now(),
        hashed_password: str = "hash"
    ) -> db.ChatInDB:
        chat = db.ChatInDB(
            id=id,
            name=name,
            owner_id=owner_id,
            owner=owner,
            created_at=created_at,
            hashed_password=hashed_password
        )

        session.add(chat)
        session.commit()
        session.refresh(chat)

        return chat

    return _build_chat

