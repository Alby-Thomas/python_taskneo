from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from document_uploader.db.database import Base


class Document(Base):
    """
    Represents a document in the system.

    :param id: The unique identifier for the document.
    :param title: The title of the document.
    :param content: The content of the document.
    :param owner_id: The ID of the user who owns the document.
    :param owner: The user who owns the document.
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

    # Define the many-to-one relationship with User
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="documents")
