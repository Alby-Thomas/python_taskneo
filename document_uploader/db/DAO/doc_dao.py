from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from document_uploader.db.models.doc_model import Document
from document_uploader.db.models.user_model import User
from document_uploader.web.api.document.document_schema import DocumentCreate

HTTP_STATUS_CODE_NOT_FOUND = 404


async def create_document(
    db: Session,
    document_data: DocumentCreate,
    current_user: User,
) -> Document:
    """
    Create a new document.

    :param db: The database session.
    :param document_data: The data for creating the document.
    :param current_user: The authenticated user.
    :return: The created document.
    """
    new_document = Document(
        title=document_data.title,
        content=document_data.content,
        owner_id=current_user.id,
    )

    db.add(new_document)
    await db.commit()
    db.refresh(new_document)

    return new_document


async def get_document(db: Session, document_id: int, current_user: User) -> Document:
    """
    Retrieve a document by its ID.

    :param db: The database session.
    :param document_id: The ID of the document to retrieve.
    :param current_user: The authenticated user.
    :return: The document with the specified ID.
    :raises HTTPException: If the document is not found or not have access.
    """
    query = select(Document).filter(Document.id == document_id)
    document = await db.execute(query)
    document = document.scalars().first()

    if not document or current_user.id != document.owner_id:
        raise HTTPException(
            status_code=HTTP_STATUS_CODE_NOT_FOUND,
            detail="Document not found",
        )

    return document


async def list_user_documents(db: Session, current_user: User) -> list[dict]:
    """
    List documents owned by a user.

    :param db: The database session.
    :param current_user: The authenticated user.
    :return: A list of documents owned by the user.
    """
    documents = await db.execute(
        select(Document).filter(Document.owner_id == current_user),
    )
    documents = documents.all()

    document_dicts = []
    for doc in documents:
        document_dicts.append(
            {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "owner_id": doc.owner_id,
            },
        )

    return document_dicts
