import strawberry


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
@strawberry.type
class Mutation:
    from .documentGQLmodel import (
        document_insert,
        document_update,
        document_delete,
        dspace_add_bitstream,
        dspace_get_bitstream,
        community_insert,
        collection_insert,
    )

    document_insert = document_insert
    document_update = document_update
    document_delete = document_delete
    dspace_add_bitstream = dspace_add_bitstream
    community_insert = community_insert
    collection_insert = collection_insert


@strawberry.type(description="""Type for query root""")
class Query:
    from .documentGQLmodel import (
        documents_page,
        document_by_id,
        dspace_get_bitstream,
        communities_page,
        collections_page,
    )

    documents_page = documents_page
    document_by_id = document_by_id
    dspace_get_bitstream = dspace_get_bitstream
    communities_page = communities_page
    collections_page = collections_page

    from .documentFolderGQLmodel import document_folder_by_id

from uoishelpers.schema import WhoAmIExtension

extensions = []
schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
