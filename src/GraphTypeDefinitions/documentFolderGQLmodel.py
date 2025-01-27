import typing
import strawberry
import uuid
from uoishelpers.resolvers import getLoadersFromInfo

DocumentGQLModel=typing.Annotated["DocumentGQLModel", strawberry.lazy(".documentGQLmodel")]

@strawberry.type(description="Document folder")
class DocumentFolderGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).documents
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        result = None
        if id is not None:
            loader = getLoadersFromInfo(info=info).document_folders
            # print(loader, flush=True)
            if isinstance(id, str):
                id = uuid.UUID(id)
            result = await loader.load(id)
            if result is not None:
                result._type_definition = cls._type_definition  # little hack :)
                result.__strawberry_definition__ = (
                    cls._type_definition
                )  # some version of strawberry changed :(
        return result
    
    id: strawberry.ID
    name: str
    description: str
    group_id: strawberry.ID
    parent_id: strawberry.ID
    created: str
    lastchange: str

    @strawberry.field(description="List of documents in the folder")
    async def documents(self, info) -> typing.List["DocumentGQLModel"]:
        from .documentGQLmodel import DocumentGQLModel
        loader = getLoadersFromInfo(info).documents
        results = await loader.filter_by(folder_id=self.id)
        return results
    

document_folder_by_id=strawberry.field(
    description="List of document folders",
    resolver=DocumentFolderGQLModel.resolve_reference,
    graphql_type=typing.Optional[DocumentFolderGQLModel],
    )