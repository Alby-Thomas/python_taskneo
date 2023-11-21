import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from document_uploader.db.dependencies import get_db_session
from document_uploader.db.models.user_model import User


async def get_user_details(
    session: AsyncSession = Depends(get_db_session),
    user_id: uuid.UUID = None,
) -> User:
    """
    Retrieve user details by user ID.

    :param session: AsyncSession - The database session (depends on `get_db_session`).
    :param user_id: UUID - The ID of the user to retrieve.
    :return: User - The user with the specified ID, or None if not found.
    """
    stmt = select(User).filter(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(
    user_details: dict,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """
    Create a new user.

    :param user_details: dict - User details including 'user_name' and 'password'.
    :param session: AsyncSession - The database session (depends on `get_db_session`).
    """
    user = User(
        id=uuid.uuid4(),
        username=user_details["user_name"],
        hashed_password=user_details["password"],
    )

    # Add the new user to the session and commit
    session.add(user)
    await session.commit()
