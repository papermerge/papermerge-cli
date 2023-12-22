from papermerge_cli import rest


def perform_server_version_command(
    host: str,
    token: str
):
    return rest.get_server_version(host=host, token=token)
