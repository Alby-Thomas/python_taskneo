from pydantic import BaseModel


class DocumentBase(BaseModel):
    """Base schema for a document."""


class DocumentCreate(DocumentBase):
    """Schema for creating a document."""


class DocumentResponse(BaseModel):
    """Schema for a document response."""

    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        """Pydantic configuration for DocumentResponse."""
