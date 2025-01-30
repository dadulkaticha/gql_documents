from uoishelpers.dataloaders import createIdLoader
from functools import cache

from src.DBDefinitions.documentDBModel import (
    DocumentModel, DocumentFolderModel
)


def createLoaders(asyncSessionMaker):
    class Loaders:
        @property
        @cache
        def DocumentModel(self):
            return createIdLoader(asyncSessionMaker, DocumentModel)
        @property
        @cache
        def document_folders(self):
            return createIdLoader(asyncSessionMaker, DocumentFolderModel)
    return Loaders()


def createLoadersContext(asyncSessionMaker):
    return {"loaders": createLoaders(asyncSessionMaker)}
