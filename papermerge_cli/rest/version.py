from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema.version import Version
from papermerge_cli.utils import host_required, token_required


@host_required
@token_required
def get_server_version(
    host: str,
    token: str
) -> Version:
    """Returns current user instance"""
    api_client = ApiClient[Version](token=token, host=host)
    version = api_client.get('/api/version/', response_model=Version)

    return version
