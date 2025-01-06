import strawberry
import datetime
import uuid
import typing
from typing import Union, Optional, List


import gql_documents.GraphTypeDefinitions
from DspaceAPI.Reguests import (
    createWorkspaceItem,
    addTitleItem,
    updateTitleItem,
    getItem,
    addBundleItem,
    getBundleId,
    addBitstreamsItem,
    getBitstreamItem,
    downloadItemContent,
    updateDescriptionItem,
    addDescriptionItem,
    setWithdrawnItem,
    getCommunities,
    createCommunity,
    createCollection,
    getCollections,
    createItem,
)


def getLoaders(info):
    return info.context["loaders"]

#from uoishelpers.resolvers import getLoader
DocumentFolderGQLModel = typing.Annotated["DocumentFolderGQLModel", strawberry.lazy('.documentFolderGQLmodel')]

###########################################################################################################################
#
# zde definujte sve nove GQL modely, kde mate zodpovednost
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
###########################################################################################################################


@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a document""",
)
class DocumentGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoaders(info).documents
    
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        result = None
        if id is not None:
            loader = getLoaders(info=info).documents
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

    @strawberry.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.i
    
    @strawberry.field(description="""Type of the document""")
    def document_type(self) -> str:
        return self.document_type

    @strawberry.field(description="""Brief description""")
    def description(self) -> Optional[str]:
        return self.description

    @strawberry.field(description="""Document Name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Initial timestamp""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberry.field(description="""Author of the document""")
    def author_id(self) -> uuid.UUID:
        # sync method which returns Awaitable :)
        return self.author_id
    
    @strawberry.field(description="""Group of the document""")
    def group_id(self) -> uuid.UUID:
        # sync method which returns Awaitable :)
        return self.group_id

    @strawberry.field(description="""DSpace id""")
    def dspace_id(self) -> uuid.UUID:
        return self.dspace_id
    
    @strawberry.field(description="""DSpace id""")
    async def folder(self) -> typing.Optional["DocumentFolderGQLModel"]:
        return None


@strawberry.input(description="""Input for document creation""")
class DocumentInsertGQLModel:
    description: Optional[str] = strawberry.field(
        default=None, description="Brief description of document"
    )
    name: str = strawberry.field(default="Name", description="Document name")
    author_id: Optional[uuid.UUID] = strawberry.field(
        default=None, description="ID of Author"
    )
    group_id: Optional[uuid.UUID] = strawberry.field(default=None, description="Owner group ID")


@strawberry.input(description="""Input for document update""")
class DocumentUpdateGQLModel:
    id: uuid.UUID = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(
        default=None, description="Timestamp"
    )
    description: Optional[str] = strawberry.field(
        default=None, description="Brief description of document"
    )
    name: Optional[str] = strawberry.field(default=None, description="Document name")
    author_id: Optional[uuid.UUID] = strawberry.field(
        default=None, description="ID of Author"
    )
    group_id: Optional[uuid.UUID] = strawberry.field(default=None, description="Owner group ID")


@strawberry.type(description="""Result of operation""")
class DocumentResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(
        default=None, description="Primary key of table row"
    )
    msg: str = strawberry.field(
        default=None, description="""result of operation, should be "ok" or "fail" """
    )

    dspace_response: str = strawberry.field(
        default=None, description="""DSPACE response JSON to DICT"""
    )

    @strawberry.field(description="""Result of drone operation""")
    async def document(
        self, info: strawberry.types.Info
    ) -> Union[DocumentGQLModel, None]:
        result = await DocumentGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.type(description="""Result of operation""")
class DspaceResultModel:
    msg: str = strawberry.field(default=None, description="""status of operation""")

    response: Optional[str] = strawberry.field(
        default=None, description="""DSPACE response JSON in list"""
    )


#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Rows of documents""")
async def documents_page(
    self,
    info: strawberry.types.Info,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[DocumentGQLModel]:
    loader = getLoaders(info).documents
    rows = await loader.page(skip=skip, limit=limit)

    return rows


@strawberry.field(description="""Returns document by id""")
async def document_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Optional[DocumentResultGQLModel]:
    result = DocumentResultGQLModel()
    document = await DocumentGQLModel.resolve_reference(info, id)

    response_json = await getItem(document.dspace_id)
    result.dspace_response = str(response_json)

    if result.dspace_response is None:
        result.msg = "Fail"
        result.id = None

    else:
        result.msg = "Ok"
        result.id = id

    return result


@strawberry.field(description="Get bitstream from dpsace")
async def dspace_get_bitstream(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Optional[DspaceResultModel]:

    result = DspaceResultModel()
    document = await DocumentGQLModel.resolve_reference(info, id)
    
    # get budle id WARNING: HARDCODED [0] its a list!
    response_json = await getBundleId(document.dspace_id)
    print(response_json)
    bundlesId = response_json["response"]["_embedded"]["bundles"][0]["uuid"]


    # get bistream id
    response_json = await getBitstreamItem(bundlesId)
    if len(response_json["response"]["_embedded"]["bitstreams"]) > 0:
        bitstreamId = response_json["response"]["_embedded"]["bitstreams"][0]["uuid"]
        bitstreamName = response_json["response"]["_embedded"]["bitstreams"][0]["name"]
    else:
        result.msg = "No Content"
        return result

    # download specific bitstream content
    response = await downloadItemContent(bitstreamId, bitstreamName)
    result.response = response["response"]
    if response["msg"] == 200:
        result.msg = "Ok"
    elif response["msg"] == 204:
        result.msg = "No Content"
    elif response["msg"] == 401:
        result.msg = "Unauthorized"
    elif response["msg"] == 403:
        result.msg = "Forbidden"
    elif response["msg"] == 404:
        result.msg = "Not found"

    return result


@strawberry.field(description="""communities""")
async def communities_page(
    self,
    info: strawberry.types.Info,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> DspaceResultModel:
    result = DspaceResultModel()

    response = await getCommunities()
    # size of communities

    totalElements = response["response"]["page"]["totalElements"]

    communities = []

    # insert community uuid and name to a list to view in GQL endpoint
    for element in range(totalElements):
        uuid = response["response"]["_embedded"]["communities"][element]["uuid"]
        name = response["response"]["_embedded"]["communities"][element]["name"]
        communities.append({uuid, name})

    result.response = str(communities)

    if response["msg"] == 200:
        result.msg = "Ok"
    elif response["msg"] == 204:
        result.msg = "No Content"
    elif response["msg"] == 401:
        result.msg = "Unauthorized"
    elif response["msg"] == 403:
        result.msg = "Forbidden"
    elif response["msg"] == 404:
        result.msg = "Not found"

    return result


@strawberry.field(description="""collections""")
async def collections_page(
    self,
    info: strawberry.types.Info,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> DspaceResultModel:
    result = DspaceResultModel()

    response = await getCollections()
    # size of communities

    totalElements = response["response"]["page"]["totalElements"]

    collections = []

    # insert community uuid and name to a list to view in GQL endpoint
    for element in range(totalElements):
        uuid = response["response"]["_embedded"]["collections"][element]["uuid"]
        name = response["response"]["_embedded"]["collections"][element]["name"]
        collections.append({uuid, name})

    result.response = str(collections)

    if response["msg"] == 200:
        result.msg = "Ok"
    elif response["msg"] == 204:
        result.msg = "No Content"
    elif response["msg"] == 401:
        result.msg = "Unauthorized"
    elif response["msg"] == 403:
        result.msg = "Forbidden"
    elif response["msg"] == 404:
        result.msg = "Not found"

    return result


#####################################################################
#
# Mutation section
#
#####################################################################
from uoishelpers.resolvers import Insert, InsertError
from uoishelpers.resolvers import Update, UpdateError
from uoishelpers.resolvers import Delete, DeleteError

@strawberry.mutation(description="Defines a new document")
async def document_insert(
    self,
    info: strawberry.types.Info,
    document: DocumentInsertGQLModel,
    collectionId: uuid.UUID,
    type: Optional[str],
    language: Optional[str],
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents
    result = DocumentResultGQLModel()

    # DSpace reguest to create an item and returns its uuid
    response = await createItem(
        collectionId=collectionId,
        title=document.name,
        author=document.author_id,
        type=type,
        language=language,
    )

    # seperate id from response
    itemId = response["response"]["uuid"]

    if isinstance(itemId, str):
        itemId = uuid.UUID(itemId)
    document.dspace_id = itemId
    result.dspace_response = str(response["response"])
    # await addTitleItem(itemsId=itemId, titleName=document.name)
    await addDescriptionItem(itemsId=itemId, description=document.description)

    await addBundleItem(itemsId=itemId)

    row = await loader.insert(document)

    if row is None:
        result.id = None
        result.msg = "Fail"
    else:
        result.id = row.id
        result.msg = "Ok"
    return result


@strawberry.mutation(description="Update existing document")
async def document_update(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel) -> typing.Union[DocumentResultGQLModel, UpdateError[DocumentResultGQLModel]]:
    loader = getLoaders(info).documents

    newName = document.name
    newDescription = document.description

    document = await DocumentGQLModel.resolve_reference(info, document.id)

    # DSPACE API reguest to update item name/title
    if newName != None:
        document.name = newName
        response_status = await updateTitleItem(document.dspace_id, newName)

    # DSPACE API reguest to update description
    if newDescription != None:
        document.description = newDescription
        response_status = await updateDescriptionItem(
            document.dspace_id, newDescription
        )

    result = DocumentResultGQLModel()
    row = await loader.update(document)
    if row is None:
        result.id = None
        result.msg = "Fail"
    else:
        result.id = row.id
        result.msg = "Ok"

    return result


@strawberry.mutation(description="Add bitstream to dpsace")
async def dspace_add_bitstream(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel, filename: str
) -> DspaceResultModel:
    result = DspaceResultModel()

    document = await DocumentGQLModel.resolve_reference(info, document.id)

    # get budle id
    response_json = await getBundleId(document.dspace_id)
    bundleId = response_json["response"]["_embedded"]["bundles"][0]["uuid"]

    # add bitstream to that bundle
    response = await addBitstreamsItem(bundleId=bundleId, filename=filename)

    result.response = str(response["response"])

    if response["msg"] == 201:
        result.msg = "Ok"
    elif response["msg"] == 400:
        result.msg = "Bad Request"
    elif response["msg"] == 401:
        result.msg = "Unauthorized"
    elif response["msg"] == 403:
        result.msg = "Forbidden"
    elif response["msg"] == 404:
        result.msg = "Not found"

    return result


@strawberry.mutation(description="Create new comunnity")
async def community_insert(
    self, info: strawberry.types.Info, name: str, language: str) -> typing.Union [DspaceResultModel, InsertError[DspaceResultModel]]:
    result = DspaceResultModel()

    response = await createCommunity(name, language)
    result.response = str(response["response"])

    if response["msg"] == 201:
        result.msg = "Ok"
    elif response["msg"] == 401:
        result.msg = "Unauthorized"

    return result


@strawberry.mutation(description="Create new collection")
async def collection_insert(
    self, info: strawberry.types.Info, parentId: uuid.UUID, name: str, language: str) -> typing.Union [DspaceResultModel, InsertError[DspaceResultModel]]:
    result = DspaceResultModel()

    response = await createCollection(parentId=parentId, name=name, language=language)

    result.response = str(response["response"])

    if response["msg"] == 201:
        result.msg = "Ok"
    elif response["msg"] == 401:
        result.msg = "Unauthorized"
    elif response["msg"] == 403:
        result.msg = "Forbidden"
    elif response["msg"] == 422:
        result.msg = "UNPROCESSABLE ENTITY"

    return result


@strawberry.mutation(description="Deletes a document")
async def document_delete(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel) -> typing.Union [DocumentResultGQLModel, DeleteError[DocumentResultGQLModel]]:
    loader = getLoaders(info).documents
    result = DocumentResultGQLModel()
    rows = await loader.filter_by(id=document.id)
    row = next(rows, None)

    if row is not None:
        response_status = await setWithdrawnItem(itemId=row.dspace_id, value="true")

        if response_status["msg"] == 200:
            row = await loader.delete(row.id)
            result.msg = "Ok"

    else:
        result.id = None
        result.msg = "Fail"

    return result
