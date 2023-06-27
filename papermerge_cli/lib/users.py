from papermerge_cli.rest import get_me
from papermerge_cli.schema import User


def me(
    host: str,
    token: str
) -> User:
    user: User = get_me(host=host, token=token)
    return user
