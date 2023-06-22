from papermerge_cli.schema import User
from papermerge_cli.fetch import get_me


def me(
    host: str,
    token: str
) -> User:
    user: User = get_me(host=host, token=token)
    return user
