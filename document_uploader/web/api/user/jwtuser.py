from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from document_uploader.db.dependencies import get_db_session
from document_uploader.db.models.user_model import User
from document_uploader.settings import settings

SECRET_KEY = "eVtGqRy5BuZp8vJ1MnAs4D"  # Replace with a strong and secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Create a CryptContext instance for password hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    return password_context.hash(password)


# Function to verify a plain password against a hashed one
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


# Function to create an access token with the provided data
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Function to decode and verify an access token
def decode_access_token(token: str) -> dict:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        return None


# Dependency function to get the current user from a valid access token
async def get_current_user(
    authorization: Annotated[
        str | None,
        Header(
            alias="Authorization",
            description="Token for authorization",
        ),
    ] = None,
    db: Session = Depends(get_db_session),
) -> User:

    payload = decode_access_token(authorization)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# Function to get a user by username
async def get_user_by_username(db: AsyncSession, username: str) -> User:
    user = await db.execute(User.__table__.select().where(User.username == username))
    return user.scalar()
