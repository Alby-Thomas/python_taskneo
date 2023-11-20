from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from document_uploader.db.dependencies import get_db_session
from document_uploader.db.models.user_model import User
from document_uploader.web.api.user.jwtuser import (
    create_access_token,
    hash_password,
    verify_password,
)
from document_uploader.web.api.user.user_schema import (
    TokenResponse,
    UserLogin,
    UserSignup,
)

router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
async def signup(user: UserSignup, db: AsyncSession = Depends(get_db_session)):
    # Check if the user already exists
    existing_user = await db.execute(
        User.__table__.select().where(User.username == user.username),
    )
    existing_user = existing_user.scalar()

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already registered")

    # Hash the user's password
    hashed_password = hash_password(user.password)

    # Create the user in the database with the hashed password
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Return an access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db_session)):
    # Retrieve the user by username from the database
    # async with db.begin() as conn:
    stmt = User.__table__.select().where(User.username == user.username)

    existing_user = await db.execute(stmt)

    existing_user = existing_user.first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Verify the password
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Return an access token upon successful login
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
