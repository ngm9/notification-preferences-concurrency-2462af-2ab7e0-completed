from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    get_current_user,
    verify_password,
)
from app.database import Base, engine, get_db
from app.models import User
from app.schemas import (
    LoginRequest,
    PreferencePatch,
    PreferenceResponse,
    TokenResponse,
)
from app.service import read_preference, update_preference


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convenient for a local demo only.
    # Use Alembic migrations in production.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Secure Notification Preferences API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/auth/token", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
):
    # This example uses globally unique email addresses.
    # If your application allows the same email in multiple tenants,
    # use tenant-aware login or your existing identity provider.
    user = db.scalar(
        select(User).where(
            User.email == str(credentials.email),
            User.is_active.is_(True),
        )
    )

    if (
        user is None
        or not verify_password(
            credentials.password,
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(user.id)
    )


@app.get(
    "/preferences/{preference_id}",
    response_model=PreferenceResponse,
)
def get_preferences(
    preference_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return read_preference(
        db,
        current_user,
        preference_id,
    )


@app.patch(
    "/preferences/{preference_id}",
    response_model=PreferenceResponse,
)
def patch_preferences(
    preference_id: int,
    payload: PreferencePatch,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return update_preference(
        db,
        current_user,
        preference_id,
        payload,
    )
