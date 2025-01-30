import asyncio
import dataclasses
import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)


#°_°
from .BaseGQLModel import BaseGQLModel, IDType


# GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".GroupGQLModel")]
# EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
# DocumentTypeGQLModel = typing.Annotated["DocumentTypeGQLModel", strawberry.lazy(".DocumentTypeGQLModel")]
# DocumentEventStateTypeGQLModel = typing.Annotated["DocumentEventStateTypeGQLModel", strawberry.lazy(".DocumentEventStateTypeGQLModel")]
# DocumentEventGQLModel = typing.Annotated["DocumentEventGQLModel", strawberry.lazy(".DocumentEventGQLModel")]

# region DocumentGQLModel
@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Document"""
)
class DocumentGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DocumentModel
 
    dspace_id: typing.Optional[IDType] = strawberry.field(
        description="primary key", 
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
        )
    
    author_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="ID of the author of the document",
        permission_classes=[OnlyForAuthentized]
    )
    
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document eng name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
        )
    
    group_id: typing.Optional[IDType] = strawberry.field(
        description="ID of the group the document belongs to",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    folder_id: typing.Optional[IDType] = strawberry.field(
        description="ID of the folder the document belongs to",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    description: typing.Optional[str] = strawberry.field(
        description="Brief description of the document",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    document_type: typing.Optional[str] = strawberry.field(
        description="Type of the document",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    created: typing.Optional[datetime.date] = strawberry.field(
        description="Creation timestamp",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    lastchange: typing.Optional[datetime.date] = strawberry.field(
        description="Last change timestamp",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )
        
    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document full name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
        )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Document datetime """,
        permission_classes=[
            OnlyForAuthentized
        ]
        )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Document datetime """,
        permission_classes=[
            OnlyForAuthentized
        ]
        )

    # address
    address: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Document address""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    # valid
    valid: typing.Optional[bool] = strawberry.field(
        default=None,
        description="""is the Document still valid""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    capacity: typing.Optional[int] = strawberry.field(
        default=None,
        description="""Document's capacity""",
        permission_classes=[
            OnlyForAuthentized
            ]
    )

    # manager_id

    # address
# geometry: typing.Optional[str] = strawberry.field(
#     default=None,
#     description="""Document geometry (SVG)""",
#     permission_classes=[
#         OnlyForAuthentized
#         ]
# )

# geolocation: typing.Optional[str] = strawberry.field(
#     default=None,
#     description="""Document geo address (WGS84+zoom)""",
#     permission_classes=[
#         OnlyForAuthentized
#         ]
# )

# group_id: typing.Optional[IDType] = strawberry.field(
#     default=None,
#     description="""Document geo address (WGS84+zoom)""",
#     permission_classes=[
#         OnlyForAuthentized
#         ]
# )

# Documenttype_id: typing.Optional[IDType] = strawberry.field(
#     default=None,
#     description="""Document geo address (WGS84+zoom)""",
#     permission_classes=[
#         OnlyForAuthentized
#         ]
# )

# master_Document_id: typing.Optional[IDType] = strawberry.field(
#     default=None,
#     description="""Document geo address (WGS84+zoom)""",
#     permission_classes=[
#         OnlyForAuthentized
#         ]
# )

# type: typing.Optional["DocumentTypeGQLModel"] = strawberry.field(
#     description="""Document type""",
#     permission_classes=[
#         OnlyForAuthentized
#         ],
#     resolver=ScalarResolver["DocumentTypeGQLModel"](fkey_field_name="Documenttype_id")
# )

# master_Document: typing.Optional["DocumentGQLModel"] = strawberry.field(
#     description="""Document above this""",
#     permission_classes=[
#         OnlyForAuthentized
#     ],
#     resolver=ScalarResolver["DocumentGQLModel"](fkey_field_name="master_Document_id")
# )

# sub_facilities: typing.List["DocumentGQLModel"] = strawberry.field(
#     description="""Facilities inside Document (like buildings in an areal)""",
#     permission_classes=[
#         OnlyForAuthentized
#         ],
#     resolver=VectorResolver["DocumentGQLModel"](fkey_field_name="master_Document_id", whereType=None)
# )

# group: typing.Optional["GroupGQLModel"] =strawberry.field(
#     description="""Document management group""",
#     permission_classes=[
#         OnlyForAuthentized
#         ],
#     resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="group_id")
# )




@createInputs
@dataclasses.dataclass
class DocumentInputFilter:
    name: str
    name_en: str
    valid: bool
    label: str
    capacity: int
    group_id: IDType
    master_Document_id: IDType
    Documenttype_id: IDType

document_by_id = strawberry.field(
        description="""Finds an Document their id""",
        permission_classes=[OnlyForAuthentized],
        graphql_type=typing.Optional[DocumentGQLModel],
        resolver=DocumentGQLModel.load_with_loader
        )

document_folder_by_id = strawberry.field(
        description="""Finds an Folder their id""",
        permission_classes=[OnlyForAuthentized],
        graphql_type=typing.Optional[DocumentGQLModel],
        resolver=DocumentGQLModel.load_with_loader
        )

document_page = strawberry.field(
        description="""Finds paged facilities""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[DocumentGQLModel](whereType=DocumentInputFilter)
        )    

# region Document
@strawberry.input(description="initial attributes for Document insert")
class DocumentInsertGQLModel:
    name: str = strawberry.field(description="name of the new Document")
    documenttype_id: typing.Optional[IDType] = strawberry.field(description="Document type", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="primary key (UUID), could be client generated", default=None)

    name_en: typing.Optional[str] = strawberry.field(description="english name of Document", default="")
    label: typing.Optional[str] = strawberry.field(description="full name (including masterDocument)", default="")
    address: typing.Optional[str] = strawberry.field(description="postal address", default="")
    valid: typing.Optional[bool] = strawberry.field(description="if Document exists", default=True)
    capacity: typing.Optional[int] = strawberry.field(description="Document capacity", default=0)
    geometry: typing.Optional[str] = strawberry.field(description="SVG overlay for leaflet", default="")
    geolocation: typing.Optional[str] = strawberry.field(description="WSGBLX;WGSBLY;ZOOM", default="")

    group_id: typing.Optional[IDType] = strawberry.field(description="group which is responsible for management of this Document", default=None)
    master_Document_id: typing.Optional[IDType] = strawberry.field(description="to which Document this Document belongs", default=None)
    rbacobject_id: typing.Optional[IDType] = \
        strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(description="set of updateable attributes")
class DocumentUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp")
    id: IDType = strawberry.field(description="primary key")

    name: typing.Optional[str] = strawberry.field(description="name of the new Document", default=None)
    documenttype_id: typing.Optional[IDType] = strawberry.field(description="Document type", default=None)

    name_en: typing.Optional[str] = strawberry.field(description="english name of Document", default=None)
    label: typing.Optional[str] = strawberry.field(description="full name (including masterDocument)", default=None)
    address: typing.Optional[str] = strawberry.field(description="postal address", default=None)
    valid: typing.Optional[bool] = strawberry.field(description="if Document exists", default=None)
    capacity: typing.Optional[int] = strawberry.field(description="Document capacity", default=None)
    geometry: typing.Optional[str] = strawberry.field(description="SVG overlay for leaflet", default=None)
    geolocation: typing.Optional[str] = strawberry.field(description="WSGBLX;WGSBLY;ZOOM", default=None)

    group_id: typing.Optional[IDType] = strawberry.field(description="group which is responsible for management of this Document", default=None)
    master_document_id: typing.Optional[IDType] = strawberry.field(description="to which Document this Document belongs", default=None)
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(description="attributes needed for operation delete")
class DocumentDeleteGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp")
    id: IDType = strawberry.field(description="primary key")

@strawberry.mutation(
        description="Updates the Document",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[DocumentGQLModel](roles=["administrátor", "administrátor budov"])
        ]
    )
async def document_update(self, info: strawberry.types.Info, Document: typing.Annotated[DocumentUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[DocumentGQLModel, UpdateError[DocumentGQLModel]]:
    return await Update[DocumentGQLModel].DoItSafeWay(info=info, entity=Document)

@strawberry.mutation(
        description="Creates a Document, available only for admins",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[DocumentGQLModel](roles=["administrátor", "administrátor budov"])
        ]
    )
async def document_insert(self, info: strawberry.types.Info, Document: DocumentInsertGQLModel) -> typing.Union[DocumentGQLModel, InsertError[DocumentGQLModel]]:
    Document.rbacobject_id = Document.rbacobject_id if Document.rbacobject_id else Document.group_id
    return await Insert[DocumentGQLModel].DoItSafeWay(info=info, entity=Document)

@strawberry.mutation(
        description="Delete the Document, available only for admins",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[DocumentGQLModel](roles=["administrátor", "administrátor budov"])
        ]
    )
async def document_delete(self, info: strawberry.types.Info, Document: DocumentDeleteGQLModel) -> typing.Optional[DeleteError[DocumentGQLModel]]:
    return await Delete[DocumentGQLModel].DoItSafeWay(info=info, entity=Document)



# class RBACUpdatePermission(SimpleUpdatePermission):
#     async def has_permission(
#         self, source: typing.Any, info: strawberry.types.Info, **kwargs: typing.Any
#     ) -> typing.Union[bool, typing.Awaitable[bool]]:
#         cls = type(self)
#         loader = cls.getLoader(info=info)
#         first_item = next(iter(kwargs.values()), None)
#         assert first_item is not None, f"item to update is unknown {kwargs}"
#         dbrow = await loader.load(first_item.id)
#         rbacobject_id = getattr(dbrow, "rbacobject_id", None)
#         pass        

# endregion
 