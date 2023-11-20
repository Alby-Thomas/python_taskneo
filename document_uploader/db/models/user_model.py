from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from document_uploader.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Store the hashed password

    # Define the one-to-many relationship with Document
    documents = relationship("Document", back_populates="owner")
