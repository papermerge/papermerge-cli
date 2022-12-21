import click
from papermerge_restapi_client.exceptions import ApiException

def pretty_breadcrumb(path: tuple) -> str:
    return f"/{'/'.join(path)}"


def sanitize_host(host: str) -> str:
    """Remove unnecessary characters from host name

    Unnecessary characters may be one or multiple whitespaces,
    or one/multiple slashes at the end of the host name.
    """
    host = host.strip()
    if host[-1] == '/':
        clean_host = host[0:-1]
        # just in case there are more trailing slash characters...
        return sanitize_host(clean_host)

    return host


def auth_required(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except ApiException as e:
            if e.status == 401:
                click.echo(
                    "Unable to authenticate.\n"
                    "Did you set PAPERMERGE_CLI__HOST"
                    " and PAPERMERGE_CLI__TOKEN?"
                )
                return
            print(e)
            return
        return result

    return inner
