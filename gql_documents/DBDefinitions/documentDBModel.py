import sqlalchemy
from sqlalchemy import Column, String, DateTime, Uuid
from .UUID import UUIDColumn
from .Base import BaseModel


class DocumentModel(BaseModel):
    __tablename__ = "documents"

    id = UUIDColumn()
    dspace_id = Column(Uuid, index=True, comment="ID of the document in the DSpace repository")

    name = Column(String, comment="Name of the document")
    author_id = Column(Uuid, index=True, nullable=True, comment="ID of the author of the document")
    group_id = Column(Uuid, index=True, nullable=True, comment="ID of the group the document belongs to")
    description = Column(String, comment="Brief description of the document")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the document was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the document was last changed")
    changed_by = Column(Uuid, index=True, comment="ID of the user who last changed the document")
    document_type = Column(String, comment="Type of the document")