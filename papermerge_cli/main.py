import os
from pathlib import Path

import click
import pkg_resources
from rich.console import Console

import papermerge_cli.format.nodes as format_nodes
import papermerge_cli.format.users as format_users
from papermerge_cli.lib.importer import upload_file_or_folder
from papermerge_cli.lib.nodes import list_nodes
from papermerge_cli.lib.users import me as perform_me
from papermerge_cli.schema import Node, Paginator, User

from .depricated_rest import (perform_download, perform_pref_list,
                              perform_pref_update, perform_search)
from .utils import sanitize_host

console = Console()

PREFIX = 'PAPERMERGE_CLI'


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    '--host',
    envvar=f'{PREFIX}__HOST',
    help='URL to REST API host. It ends with slash and it includes protocol'
    'scheme as well. For example: http://localhost:8000/'
)
@click.option(
    '-t', '--token',
    default=lambda: os.environ.get('TOKEN', None),
    envvar=f'{PREFIX}__TOKEN',
    help='JWT authorization token.'
)
@click.option(
    '--version',
    help='Show version of the papermerge-cli',
    is_flag=True
)
def cli(ctx, host, token, version):
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


@click.command(name="import")
@click.argument('file_or_folder', type=click.Path(exists=True))
@click.option(
    '--delete',
    is_flag=True,
    help='Delete local(s) file after successful upload.',
)
@click.option(
    '--target-id',
    help="UUID of the target/destination folder. "
         "Default value is user's Inbox folder's UUID.",
)
@click.pass_context
def _import(ctx, file_or_folder, delete, target_id):
    """Import recursively documents from local folder

    If target UUID (--target-uuid) is not provided, target node UUID
    defaults to the user's inbox folder UUID. In other words, import will
    upload all documents to the user's inbox - if you want to change that, you
    need to provide UUID of the folder where you want to upload
    documents to.
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


@click.command(name="list")
@click.option('--parent-id', help='Parent folder UUID')
@click.option('--inbox', help='List nodes from Inbox folder', is_flag=True)
@click.option('--page-number', help='Page number to list', default=1)
@click.option('--page-size', help='Page size', default=15)
@click.pass_context
def _list(ctx, parent_id, inbox, page_number, page_size):
    """Lists documents and folders of the given node

    If in case no specific node is requested - will list content
    of the user's home folder.
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


@click.command(name="me")
@click.pass_context
def current_user(
    ctx
):
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
    """List preferences"""
    token = ctx.obj.get('TOKEN', None)
    host = ctx.obj.get('HOST', None)
    perform_pref_list(
        host=host,
        token=token,
        section=section,
        name=name
    )


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
    """List preferences"""
    token = ctx.obj.get('TOKEN', None)
    host = ctx.obj.get('HOST', None)
    perform_pref_update(
        host=host,
        token=token,
        section=section,
        name=name,
        value=value
    )


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
    """Search for document or folder containing given text"""
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    perform_search(
        host=host,
        token=token,
        query=query,
        tags=tags,
        tags_op=tags_op
    )


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
    """Download one or multiple nodes"""
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
