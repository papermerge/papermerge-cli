from typing import List
from uuid import UUID

from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema import CreateFolder, Folder, Node, Paginator
from papermerge_cli.utils import host_required, token_required


@host_required
@token_required
def get_nodes(
    node_id: str,
    host: str,
    token: str,
    query_params
) -> Paginator[Node]:
    """Returns children nodes of the parent node specified by `node_id`"""

    api_client = ApiClient[Paginator[Node]](token=token, host=host)
    paginator = api_client.get(
        f'/api/nodes/{node_id}',
        response_model=Paginator[Node],
        query_params=query_params
    )

    return paginator


def node_assign_tags(
    node_id: UUID,
    host: str,
    token: str,
    tags: List[str]
):
    """Assigns list of tags to the node

    Assignment operation will replace all current tags with the
    new ones.
    """
    api_client = ApiClient(token=token, host=host)
    api_client.post(
        f'/api/nodes/{node_id}/tags',
        json=tags
    )


def node_add_tags(
    node_id: UUID,
    host: str,
    token: str,
    tags: List[str]
):
    """Add list of tags to the node

    Add operation will append new tags to the current one.
    """
    api_client = ApiClient(token=token, host=host)
    api_client.patch(
        f'/api/nodes/{node_id}/tags',
        json=tags
    )


def node_remove_tags(
    node_id: UUID,
    host: str,
    token: str,
    tags: List[str]
):
    """Remove list of tags from the node"""
    api_client = ApiClient(token=token, host=host)
    api_client.delete(
        f'/api/nodes/{node_id}/tags',
        json=tags
    )


def create_folder(
    host: str,
    token: str,
    title: str,
    parent_id: UUID
) -> Folder:
    api_client = ApiClient[Folder](token=token, host=host)

    folder_to_create = CreateFolder(
        title=title,
        parent_id=parent_id
    )

    response_folder: Folder = api_client.post(
        '/api/nodes/',
        response_model=Folder,
        json=folder_to_create.model_dump(mode='json')
    )

    return response_folder


def create_document():
    pass
