import uuid
import datetime
import sqlalchemy
from sqlalchemy import Column, String, DateTime, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class DocumentModel(BaseModel):
    __tablename__ = "documents"

    # Fields with proper types and SQLAlchemy mapped columns
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, insert_default=uuid.uuid4, comment="Primary key")

    dspace_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False, default=None, comment="ID of the document in the DSpace repository")

    name: Mapped[str] = mapped_column(String, nullable=False, default=None, comment="Name of the document")
    
    author_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("authors.id"), nullable=True, default=None, comment="ID of the author of the document")
    group_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("groups.id"), nullable=True, default=None, comment="ID of the group the document belongs to")
    folder_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document_folders.id"), nullable=True, default=None, comment="ID of the folder the document belongs to")
    
    description: Mapped[str] = mapped_column(String, nullable=True, default=None, comment="Brief description of the document")

    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=sqlalchemy.sql.func.now(), nullable=True, default=None, comment="Date and time the document was created")
    lastchange: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=sqlalchemy.sql.func.now(), nullable=True, default=None, onupdate=sqlalchemy.sql.func.now(), comment="Date and time the document was last changed")

    document_type: Mapped[str] = mapped_column(String, nullable=True, default=None, comment="Type of the document")


class DocumentFolderModel(BaseModel):
    __tablename__ = "document_folders"

    # Fields with mapped types and proper comments
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, insert_default=uuid.uuid4, comment="Primary key")

    name: Mapped[str] = mapped_column(String, nullable=True, default= None, comment="Name of the folder")
    description: Mapped[str] = mapped_column(String, nullable=True, default= None, comment="Brief description of the folder")

    group_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("groups.id"), nullable=True, default= None, comment="ID of the group the folder belongs to")
    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document_folders.id"), index=True, nullable=True, default= None, comment="ID of the parent folder")

    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=sqlalchemy.sql.func.now(), nullable= True, default= None, comment="Date and time the folder was created")
    lastchange: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=sqlalchemy.sql.func.now(), nullable= True, default= None, onupdate=sqlalchemy.sql.func.now(), comment="Date and time the folder was last changed")