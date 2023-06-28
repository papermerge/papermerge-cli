import uuid

from papermerge_cli.rest import get_me, get_nodes
from papermerge_cli.schema import Node, Paginator, User


def list_nodes(
    host: str,
    token: str,
    inbox: bool = False,
    parent_id: uuid.UUID | None = None,
    page_number: int = 1,
    page_size: int = 15,
    order_by: str = '-title'
) -> Paginator[Node]:

    user: User = get_me(host=host, token=token)

    if parent_id is None:
        # in case no specific parent uuid is requested
        # will list the content of user home's folder
        if inbox is True:
            # however, if flag `--inbox` is provided, will
            # list content of user's inbox folder
            node_id = str(user.inbox_folder_id)
        else:
            node_id = str(user.home_folder_id)
    else:
        node_id = parent_id

    query_params = {
        'page_number': page_number,
        'page_size': page_size,
        'order_by': order_by
    }

    data: Paginator[Node] = get_nodes(
        node_id=node_id,
        host=host,
        token=token,
        query_params=query_params

    )

    return data
