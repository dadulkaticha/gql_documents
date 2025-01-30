# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class BaseModel(DeclarativeBase,MappedAsDataclass):
    pass
