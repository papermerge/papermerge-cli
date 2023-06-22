from papermerge_cli.utils import (host_required, token_required, catch_401)
from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema.users import User


@catch_401
@host_required
@token_required
def get_me(
    host: str,
    token: str
) -> User:
    """Returns current user instance"""
    api_client = ApiClient[User](token=token, host=host)
    user = api_client.get('/api/users/me', response_modal=User)

    return user
