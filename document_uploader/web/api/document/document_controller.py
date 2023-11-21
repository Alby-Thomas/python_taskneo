from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from document_uploader.auth.authentication import get_current_user
from document_uploader.db.dependencies import get_db_session
from document_uploader.db.models.user_model import User
from document_uploader.services.doc_service import (
    create_document_service,
    get_document_service,
    list_user_documents_service,
)
from document_uploader.web.api.document.document_schema import (
    DocumentCreate,
    DocumentResponse,
)

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
async def create_document(
    document_data: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    """
    Endpoint to create a new document.

    :param document_data: DocumentCreate - Data for creating the document.
    :param current_user: User - The authenticated user.
    :param db: Session - The database session (depends on `get_db_session`).
    :return: DocumentResponse - The created document.
    """
    return await create_document_service(db, document_data, current_user)


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    """
    Endpoint to retrieve a document by its ID.

    :param document_id: int - The ID of the document to retrieve.
    :param current_user: User - The authenticated user.
    :param db: Session - The database session (depends on `get_db_session`).
    :return: DocumentResponse - The document with the specified ID.
    """
    return await get_document_service(db, document_id, current_user)


@router.get("/user/documents", response_model=List[DocumentResponse])
async def list_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    """
    Endpoint to list documents owned by a user.

    :param current_user: User - The authenticated user.
    :param db: Session - The database session (depends on `get_db_session`).
    :return: List[DocumentResponse] - List of documents owned by the user.
    """
    return await list_user_documents_service(db, current_user)
