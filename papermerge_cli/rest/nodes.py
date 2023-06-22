from papermerge_cli.fetch import get_me, get_nodes
from papermerge_cli.schema import Node, Paginator, User


def list_nodes(
    host: str,
    token: str,
    inbox: bool = False,
    parent_uuid: str | None = None,
    page_number: int = 1,
    page_size: int = 15
) -> Paginator[Node]:

    user: User = get_me(host=host, token=token)

    if parent_uuid is None:
        # in case no specific parent uuid is requested
        # will list the content of user home's folder
        if inbox is True:
            # however, if flag `--inbox` is provided, will
            # list content of user's inbox folder
            node_id = str(user.inbox_folder_id)
        else:
            node_id = str(user.home_folder_id)
    else:
        node_id = parent_uuid

    query_params = {
        'page_number': page_number,
        'per_page': page_size
    }

    data: Paginator[Node] = get_nodes(
        node_id=node_id,
        host=host,
        token=token,
        query_params=query_params

    )

    return data
