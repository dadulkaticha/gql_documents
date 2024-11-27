import typing
import strawberry
DocumentGQLModel=typing.Annotated["DocumentGQLModel", strawberry.lazy(".documentGQLmodel")]

@strawberry.type(description="Document folder")
class DocumentFolderGQLModel:
    id: strawberry.ID
    name: str
    description: str
    group_id: strawberry.ID
    parent_id: strawberry.ID
    created: str
    lastchange: str

    @strawberry.field(description="List of documents in the folder")
    async def documents(self, info) -> typing.List["DocumentGQLModel"]:
        return []