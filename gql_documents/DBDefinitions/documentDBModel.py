import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class DocumentModel(BaseModel):
    __tablename__ = "documents"

    id = UUIDColumn()
    dspace_id = Column(String, index=True)

    name = Column(String)
    author = UUIDFKey(nullable=True)
    description = Column(String, comment="Brief description of the document")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())