from papermerge_cli.utils import (host_required, token_required, catch_401)
from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema import Node, Paginator


@catch_401
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
        response_modal=Paginator[Node],
        query_params=query_params
    )

    return paginator
