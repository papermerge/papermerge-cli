import importlib.metadata
import uuid
from pathlib import Path
from typing import List

import click
import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

import papermerge_cli.format.nodes as format_nodes
import papermerge_cli.format.users as format_users
from papermerge_cli.lib.importer import upload_file_or_folder
from papermerge_cli.lib.nodes import list_nodes, perform_node_command
from papermerge_cli.lib.users import me as perform_me
from papermerge_cli.lib.version import perform_server_version_command
from papermerge_cli.schema import Node, Paginator, User
from papermerge_cli.types import NodeActionEnum

from .utils import sanitize_host

PREFIX = 'PAPERMERGE_CLI'

console = Console()
app = typer.Typer()


HostEnvVar = Annotated[
    str,
    typer.Option(
        envvar=f"{PREFIX}__HOST",
        help="REST API host. It ends with slash and it includes protocol"
             "scheme as well. For example: http://localhost:8000/"
    ),
]
TokenEnvVar = Annotated[
    str,
    typer.Option(
        envvar=f"{PREFIX}__TOKEN",
        help='JWT authorization token'
    ),
]
NodeAction = Annotated[
    NodeActionEnum,
    typer.Argument(
        help='add/removes/assign tags to the node'
    )
]
NodeID = Annotated[
    uuid.UUID,
    typer.Option(help='Node UUID')
]
ParentFolderID = Annotated[
    uuid.UUID,
    typer.Option(help='Parent folder UUID')
]
InboxFlag = Annotated[
    bool,
    typer.Option(is_flag=True, help='List nodes from Inbox folder')
]
PageSize = Annotated[
    int,
    typer.Option(
        min=1,
        max=1000,
        help='Results items will be listed on a single page'
    )
]
PageNumber = Annotated[
    int,
    typer.Option(
        min=1,
        max=10000,
        help='Results list page number'
    )
]
FileOrFolderPath = Annotated[
    Path,
    typer.Argument(
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Local path to file or folder to import"
    )
]
DeleteAfterImport = Annotated[
    bool,
    typer.Option(
        is_flag=True,
        help='Delete local(s) file after successful upload.'
    )
]
TargetNodeID = Annotated[
    uuid.UUID,
    typer.Option(
        help="UUID of the target/destination folder. "
             "Default value is user's Inbox folder's UUID."
    )
]
OrderBy = Annotated[
    str,
    typer.Option(
        help="Ordering criteria. Valid fields are title, ctype, created_at, "
        "updated_at. Fields can be preceeded by '-' to express reverse order."
        "For example order_by=-title, will sort restuls by title in "
        "descendant order"
    )
]


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    host: HostEnvVar,
    token: TokenEnvVar,
    version: Annotated[bool, typer.Option(is_flag=True)] = False
):
    # run sub-command
    ctx.ensure_object(dict)
    ctx.obj['HOST'] = sanitize_host(host)
    ctx.obj['TOKEN'] = token

    if ctx.invoked_subcommand is None:
        # invoked without sub-command
        if version:
            papermerge_cli_version = importlib.metadata.version(
                "papermerge-cli"
            )
            click.echo(papermerge_cli_version)
        else:
            list_nodes_command(ctx)


@app.command(name="import")
def import_command(
    ctx: typer.Context,
    file_or_folder: FileOrFolderPath,
    delete: DeleteAfterImport = False,
    target_id: TargetNodeID | None = None
):
    """Import recursively folders and documents from local filesystem

    If target UUID is not provided import will upload all documents to
    the user's inbox
    """
    try:
        upload_file_or_folder(
            host=ctx.obj['HOST'],
            token=ctx.obj['TOKEN'],
            file_or_folder=Path(file_or_folder),
            parent_id=target_id,
            delete=delete
        )
    except Exception as ex:
        console.print(ex)


@app.command(name="ls")
def list_nodes_command(
    ctx: typer.Context,
    parent_id: ParentFolderID | None = None,
    inbox: InboxFlag = False,
    page_number: PageNumber = 1,
    page_size: PageSize = 15,
    order_by: OrderBy = '-title'
):
    """Lists documents and folders from your papermerge account

    If in case no specific node is requested - will list content
    of the user's home folder
    """
    try:
        data: Paginator[Node] = list_nodes(
            host=ctx.obj['HOST'],
            token=ctx.obj['TOKEN'],
            inbox=inbox,
            parent_id=parent_id,
            page_number=page_number,
            page_size=page_size,
            order_by=order_by
        )
    except Exception as ex:
        console.print(ex, style="red")
        return

    output: Table = format_nodes.list_nodes(data)
    if len(output.rows):
        console.print(output)
    else:
        console.print("Empty folder")


@app.command(name="me")
def current_user_command(ctx: typer.Context):
    """Show details of current user"""
    try:
        user: User = perform_me(
            host=ctx.obj['HOST'],
            token=ctx.obj['TOKEN'],
        )
        output = format_users.current_user(user)
        console.print(output)
    except Exception as ex:
        console.print(ex)


@app.command(name="node")
def node_command(
    ctx: typer.Context,
    node_id: NodeID,
    action: NodeAction,
    tags: List[str]
):
    """Perform actions on specific node"""
    perform_node_command(
        host=ctx.obj['HOST'],
        token=ctx.obj['TOKEN'],
        node_id=node_id,
        action=action,
        tags=tags
    )


@app.command(name="server-version")
def server_version_command(ctx: typer.Context):
    """Get REST API version used on server side"""
    output = perform_server_version_command(
        host=ctx.obj['HOST'],
        token=ctx.obj['TOKEN'],
    )

    console.print(output)


"""
@click.command
@click.option(
    '--section',
    help='Limit output to preferences from this section only',
)
@click.option('--name', help='Limit output to preferences with this only')
@click.pass_context
def pref_list(
    ctx,
    section,
    name
):
    token = ctx.obj.get('TOKEN', None)
    host = ctx.obj.get('HOST', None)
    perform_pref_list(
        host=host,
        token=token,
        section=section,
        name=name
    )
"""

"""
@click.command
@click.pass_context
@click.option('--section', help='Section name of the preference to update')
@click.option('--name', help='Name of the preference to update')
@click.option(
    '--value',
    help='New value for the preference specified by section and name',
)
def pref_update(
    ctx,
    section,
    name,
    value
):
    token = ctx.obj.get('TOKEN', None)
    host = ctx.obj.get('HOST', None)
    perform_pref_update(
        host=host,
        token=token,
        section=section,
        name=name,
        value=value
    )
"""

"""
@click.command
@click.pass_context
@click.option('-q', '--query', help='Text to search for')
@click.option('-t', '--tags', help='Comma separated list of tags')
@click.option(
    '--tags-op', type=click.Choice(['all', 'any']), default='all',
    help='Should node contain all or any of the provided tags?',
    show_default=True
)
def search(
    ctx,
    query,
    tags,
    tags_op
):
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    perform_search(
        host=host,
        token=token,
        query=query,
        tags=tags,
        tags_op=tags_op
    )
"""


"""
@click.command
@click.pass_context
@click.option(
    '-u', '--uuid', type=click.UUID, multiple=True,
    help='UUID of the node to download. You can use this option multiple times',
)
@click.option(
    '-f', '--file-name',
    help='Name of the file where to save downloaded document/folder',
)
@click.option(
    '-t', '--archive-type', type=click.Choice(['zip', 'targz']),
    default='zip', show_default=True,
    help='Download node as tar.gz or as .zip',
)
def download(
    ctx,
    uuid: tuple[click.UUID],
    file_name: str,
    archive_type: str
):
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    perform_download(
        host=host,
        token=token,
        uuids=uuid,
        file_name=file_name,
        archive_type=archive_type
    )


cli.add_command(_import)
cli.add_command(_list)  # list nodes
cli.add_command(current_user)
cli.add_command(pref_list)
cli.add_command(pref_update)
cli.add_command(search)
cli.add_command(download)
"""
