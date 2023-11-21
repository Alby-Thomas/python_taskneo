from typing import List

from sqlalchemy.orm import Session

from document_uploader.db.DAO.doc_dao import (
    create_document,
    get_document,
    list_user_documents,
)
from document_uploader.db.models.user_model import User
from document_uploader.web.api.document.document_schema import DocumentCreate


async def create_document_service(
    db: Session,
    document_data: DocumentCreate,
    current_user: User,
) -> dict:
    """
    Create a new document.

    :param db: The database session.
    :param document_data: The data for creating a document.
    :param current_user: The authenticated user.
    :return: A dictionary containing the created document's details.
    """
    return await create_document(db, document_data, current_user)


async def get_document_service(
    db: Session,
    document_id: int,
    current_user: User,
) -> dict:
    """
    Retrieve details of a specific document.

    :param db: The database session.
    :param document_id: The ID of the document to retrieve.
    :param current_user: The authenticated user.
    :return: Details of the specified document.
    """
    return await get_document(db, document_id, current_user)


async def list_user_documents_service(db: Session, current_user: User) -> List[dict]:
    """
    List documents belonging to the current user.

    :param db: The database session.
    :param current_user: The authenticated user.
    :return: A list of dictionaries containing details of user's documents.
    """
    return await list_user_documents(db, current_user)
