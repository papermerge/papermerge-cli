from rich.console import Console

console = Console()


def pretty_breadcrumb(path: tuple) -> str:
    return f"/{'/'.join(path)}"


def sanitize_host(host: str) -> str | None:
    """Remove unnecessary characters from host name

    Unnecessary characters may be one or multiple whitespaces,
    or one/multiple slashes at the end of the host name.
    """
    if host is None:
        return host

    host = host.strip()
    if host[-1] == '/':
        clean_host = host[0:-1]
        # just in case there are more trailing slash characters...
        return sanitize_host(clean_host)

    return host


def token_required(func):
    def inner(**kwargs):
        token = kwargs.get('token', None)

        if token is None:
            console.print(
                "Neither [b]PAPERMERGE_CLI__TOKEN[/b] not set"
                " nor [b]--token[/b] option was provided",
                style="red"
            )
            return
        return func(**kwargs)

    return inner


def host_required(func):
    def inner(**kwargs):
        token = kwargs.get('host', None)

        if token is None:
            console.print(
                "Neither [b]PAPERMERGE_CLI__HOST[/b] not set"
                " nor [b]--host[/b] option was provided",
                style="red"
            )
            return
        return func(**kwargs)

    return inner
