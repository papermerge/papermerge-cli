
def pretty_breadcrumb(path: tuple) -> str:
    return f"/{'/'.join(path)}"


def sanitize_host(host: str) -> str:
    """Remove unnecessary characters from host name"""
    host = host.strip()
    if host[-1] == '/':
        host = host[0:-1]

    return host
