import typing
import strawberry
import uuid
from uoishelpers.resolvers import getLoadersFromInfo

DocumentGQLModel=typing.Annotated["DocumentGQLModel", strawberry.lazy(".documentGQLmodel")]

@strawberry.type(description="Document folder")
class DocumentFolderGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        loader = getLoadersFromInfo(info).document_folders
        if not loader:
            raise RuntimeError("Loader for document_folders not found")
        return loader

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        if not id:
            raise ValueError("Invalid ID: ID cannot be None")

        loader = cls.getLoader(info)
        folder_data = await loader.load(id)

        if not folder_data:
            raise ValueError(f"No document folder found for ID: {id}")

        # Convert database object to the GraphQL model
        return cls(**folder_data.__dict__)

    id: strawberry.ID
    name: typing.Optional[str]
    description: typing.Optional[str]
    group_id: typing.Optional[strawberry.ID]
    parent_id: typing.Optional[strawberry.ID]
    created: str
    lastchange: str

    @strawberry.field(description="List of documents in the folder")
    async def documents(self, info) -> typing.List["DocumentGQLModel"]:
        from .documentGQLmodel import DocumentGQLModel
        loader = getLoadersFromInfo(info).documents
        return await loader.filter_by(folder_id=self.id)
        return results
    
folder_page = strawberry.field(
    description="Returns a page of document folders",
    resolver=DocumentFolderGQLModel.getLoader,
    graphql_type=typing.List[DocumentFolderGQLModel],
)

document_folder_by_id = strawberry.field(
    description="Finds a document folder by its ID",
    resolver=DocumentFolderGQLModel.resolve_reference,
    graphql_type=typing.Optional[DocumentFolderGQLModel],
)
