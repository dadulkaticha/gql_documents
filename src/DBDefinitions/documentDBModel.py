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
    folder_id = Column(Uuid, index=True, nullable=True, comment="ID of the folder the document belongs to")
    description = Column(String, comment="Brief description of the document")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the document was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the document was last changed")
    #changedby_id = Column(Uuid, index=True, comment="ID of the user who last changed the document")
    document_type = Column(String, comment="Type of the document")

class DocumentFolderModel(BaseModel):
    __tablename__ = "document_folders"

    id = UUIDColumn()
    name = Column(String, comment="Name of the folder")
    description = Column(String, comment="Brief description of the folder")
    group_id = Column(Uuid, index=True, nullable=True, comment="ID of the group the folder belongs to")
    parent_id = Column(Uuid, index=True, nullable=True, comment="ID of the parent folder")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the folder was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the folder was last changed")
    #changedby_id = Column(Uuid, index=True, comment="ID of the user who last changed the folder")