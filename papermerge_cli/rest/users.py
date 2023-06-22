from rich.table import Table
from papermerge_cli.format import current_user as format_current_user
from papermerge_cli.fetch import get_me


def me(
    host: str,
    token: str
) -> Table:
    user = get_me(host=host, token=token)
    table = format_current_user(user)

    return table
