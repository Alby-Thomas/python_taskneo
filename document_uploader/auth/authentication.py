from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Header, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from document_uploader.db.dependencies import get_db_session
from document_uploader.db.models.user_model import User
from document_uploader.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Create a CryptContext instance for password hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define status code constants
UNAUTHORIZED_STATUS_CODE = 401

# Function to hash a password


def hash_password(password: str) -> str:
    """
    Hash a password.

    :param password: str - The password to hash.
    :return: str - The hashed password.
    """
    return password_context.hash(password)


# Function to verify a plain password against a hashed one


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed one.

    :param plain_password: str - The plain password to verify.
    :param hashed_password: str - The hashed password to compare against.
    :return: bool - True if the passwords match, False otherwise.
    """
    return password_context.verify(plain_password, hashed_password)


# Function to create an access token with the provided data


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create an access token with the provided data.

    :param data: dict - The data to include in the token.
    :param expires_delta: timedelta - The expiration time for the token.
    :return: str - The generated access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Function to decode and verify an access token


def decode_access_token(token: str) -> dict:
    """
    Decode and verify an access token.

    :param token: str - The access token to decode and verify.
    :return: dict - The decoded payload of the token, or None if verification fails.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:
        return None


# Dependency function to get the current user from a valid access token
HeaderAlias = Header(
    alias="Authorization",
    description="Token for authorization",
)


async def get_current_user(
    authorization: Optional[str] = Depends(HeaderAlias),
    db: Session = Depends(get_db_session),
) -> User:
    """
    Get the current user from a valid access token.

    :param authorization: str | None - The access token from the request header.
    :param db: Session - The database session (depends on `get_db_session`).
    :return: User - The authenticated user.
    :raises HTTPException: If authentication fails.
    """
    payload = decode_access_token(authorization)

    if payload is None:
        raise HTTPException(
            status_code=UNAUTHORIZED_STATUS_CODE,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=UNAUTHORIZED_STATUS_CODE,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=UNAUTHORIZED_STATUS_CODE,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# Function to get a user by username


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    """
    Get a user by username.

    :param db: AsyncSession - The database session.
    :param username: str - The username to search for.
    :return: User - The user with the specified username, or None if not found.
    """
    user = await db.execute(User.__table__.select().where(User.username == username))
    return user.scalar()
