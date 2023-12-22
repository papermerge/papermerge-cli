import uuid
from typing import List

from papermerge_cli import rest
from papermerge_cli.schema import Node, Paginator, User
from papermerge_cli.types import NodeActionEnum


def list_nodes(
    host: str,
    token: str,
    inbox: bool = False,
    parent_id: uuid.UUID | None = None,
    page_number: int = 1,
    page_size: int = 15,
    order_by: str = '-title'
) -> Paginator[Node]:

    user: User = rest.get_me(host=host, token=token)

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

    data: Paginator[Node] = rest.get_nodes(
        node_id=node_id,
        host=host,
        token=token,
        query_params=query_params

    )

    return data


def perform_node_command(
    host: str,
    token: str,
    node_id: uuid.UUID,
    action: NodeActionEnum,
    tags: List[str]
):
    if action in (NodeActionEnum.assign_tags, NodeActionEnum.replace_tags):
        rest.node_assign_tags(
            host=host,
            token=token,
            node_id=node_id,
            tags=tags
        )
    elif action in (NodeActionEnum.add_tags, NodeActionEnum.append_tags):
        rest.node_add_tags(
            host=host,
            token=token,
            node_id=node_id,
            tags=tags
        )
    elif action in (NodeActionEnum.remove_tags, NodeActionEnum.delete_tags):
        rest.node_remove_tags(
            host=host,
            token=token,
            node_id=node_id,
            tags=tags
        )
    else:
        raise ValueError("Invalid node action")
