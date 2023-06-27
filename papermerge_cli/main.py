import uuid
from pathlib import Path

import click
import pkg_resources
import typer
from rich.console import Console
from typing_extensions import Annotated

import papermerge_cli.format.nodes as format_nodes
import papermerge_cli.format.users as format_users
from papermerge_cli.lib.importer import upload_file_or_folder
from papermerge_cli.lib.nodes import list_nodes
from papermerge_cli.lib.users import me as perform_me
from papermerge_cli.schema import Node, Paginator, User

from .utils import sanitize_host

PREFIX = 'PAPERMERGE_CLI'

console = Console()
app = typer.Typer()


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
    typer.Option(min=1, max=1000, help='Results list page size')
]
PageNumber = Annotated[
    int,
    typer.Option(min=1, max=10000, help='Results list page number')
]
FileOrFolderPath = Annotated[Path, typer.Argument(exists=True)]
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


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    host: Annotated[str, typer.Option(envvar=f"{PREFIX}__HOST")],
    token: Annotated[str, typer.Option(envvar=f"{PREFIX}__TOKEN")],
    version: Annotated[bool, typer.Option(is_flag=True)] = True
):
    if ctx.invoked_subcommand is None:
        # invoked without sub-command i.e. display version
        if version:
            papermerge_cli_version = pkg_resources.get_distribution(
                'papermerge-cli'
            ).version
            click.echo(papermerge_cli_version)
    else:
        # run sub-command
        ctx.ensure_object(dict)
        ctx.obj['HOST'] = sanitize_host(host)
        ctx.obj['TOKEN'] = token


@app.command(name="import")
def _import(
    ctx,
    file_or_folder: FileOrFolderPath,
    delete: DeleteAfterImport,
    target_id: TargetNodeID
):
    """Import recursively folders and documents from local storage

    If target UUID is not provided import will upload all documents to
    the user's inbox
    """
    host = ctx.obj['HOST']
    token = ctx.obj['TOKEN']

    try:
        upload_file_or_folder(
            host=host,
            token=token,
            file_or_folder=Path(file_or_folder),
            parent_id=target_id,
        )
    except Exception as ex:
        console.print(ex)


@app.command(name="list")
def _list(
    ctx: typer.Context,
    parent_id: ParentFolderID | None = None,
    inbox: InboxFlag = False,
    page_number: PageNumber = 1,
    page_size: PageSize = 15
):
    """Lists documents and folders of the given node

    If in case no specific node is requested - will list content
    of the user's home folder
    """
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    data: Paginator[Node] = list_nodes(
        host=host,
        token=token,
        inbox=inbox,
        parent_id=parent_id,
        page_number=page_number,
        page_size=page_size
    )

    output = format_nodes.list_nodes(data)
    console.print(output)


@app.command(name="me")
def current_user(ctx: typer.Context):
    """Show details of current user"""
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    try:
        user: User = perform_me(
            host=host,
            token=token,
        )
        output = format_users.current_user(user)
        console.print(output)
    except Exception as ex:
        console.print(ex)


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
