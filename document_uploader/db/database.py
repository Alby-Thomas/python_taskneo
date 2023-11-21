from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from document_uploader.db.base import Base
from document_uploader.db.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
