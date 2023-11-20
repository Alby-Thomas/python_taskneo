from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from document_uploader.db.dependencies import get_db_session
from document_uploader.db.models.doc_model import Document
from document_uploader.db.models.user_model import (  # Adjust the import path as needed
    User,
)
from document_uploader.web.api.document.document_schema import (
    DocumentCreate,
    DocumentResponse,
)
from document_uploader.web.api.user.jwtuser import get_current_user

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
async def create_document(
    document_data: DocumentCreate,
    current_user: User = Depends(get_current_user),  # Use User type here
    db: Session = Depends(get_db_session),
):
    # Create a new document and associate it with the authenticated user

    new_document = Document(
        title=document_data.title,
        content=document_data.content,
        owner_id=current_user,
    )

    # Add the new document to the session and commit it to the database
    db.add(new_document)
    await db.commit()
    db.refresh(new_document)

    return new_document


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    # Fetch the document by ID using SQLAlchemy's select

    query = select(Document).filter(Document.id == document_id)
    document = await db.execute(query)
    document = document.scalars().first()

    # Check if the document exists and the user has permission to access it
    if not document or current_user != document_id:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


@router.get("/user/documents", response_model=List[DocumentResponse])
async def list_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    # Query the database for documents associated with the specified user
    documents = await db.execute(
        select(Document).filter(Document.owner_id == current_user),
    )
    documents = documents.all()

    # Extract the Document objects and convert them to dictionaries
    document_dicts = [
        {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "owner_id": doc.owner_id,
        }
        for doc, in documents
    ]

    return document_dicts
