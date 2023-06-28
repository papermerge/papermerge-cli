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
        json=folder_to_create.json()
    )

    return response_folder


def create_document():
    pass
