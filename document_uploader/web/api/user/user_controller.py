from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from document_uploader.db.dependencies import get_db_session
from document_uploader.services.user_service import login, signup
from document_uploader.web.api.user.user_schema import (
    TokenResponse,
    UserLogin,
    UserSignup,
)

router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
async def signup_user(user: UserSignup, db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint to register a new user.

    :param user: UserSignup - User registration data.
    :param db: AsyncSession - The async database session (depends on `get_db_session`).
    :return: TokenResponse - A dictionary containing the access token and token type.
    """
    try:
        return await signup(user, db)
    except HTTPException as error:
        return error


@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint to log in a user.

    :param user: UserLogin - User login data.
    :param db: AsyncSession - The async database session (depends on `get_db_session`).
    :return: TokenResponse - A dictionary containing the access token and token type.
    """
    try:
        return await login(user, db)
    except HTTPException as error:
        return error
