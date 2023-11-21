from sqlalchemy.orm import DeclarativeBase

from document_uploader.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
