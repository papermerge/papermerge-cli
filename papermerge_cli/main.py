import os
import click
import pkg_resources
from rich.console import Console

console = Console()

from .rest import (
    perform_auth,
    perform_list,
    perform_me,
    perform_import,
    perform_pref_list,
    perform_pref_update,
    perform_search,
    perform_download
)
from .utils import sanitize_host

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
    help='Authentication token.'
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


@click.command()
@click.option(
    '--username',
    '-u',
    prompt=True,
    help='Username'
)
@click.option(
    '--password',
    '-p',
    prompt=True,
    hide_input=True,
    confirmation_prompt=False,
    help='Password'
)
@click.pass_context
def auth(ctx, username, password):
    """Authenticate with username and password"""
    token = perform_auth(
        host=ctx.obj['HOST'],
        username=username,
        password=password
    )
    click.echo(token)


@click.command(name="import")
@click.argument('file_or_folder')
@click.option(
    '--delete',
    help='Delete local(s) file after successful upload.',
    is_flag=True,
)
@click.option(
    '--target-uuid',
    help="UUID of the target/destination folder. "
         "Default value is user's Inbox folder's UUID.",
)
@click.pass_context
def _import(ctx, file_or_folder, delete, target_uuid):
    """Import recursively documents from local folder

    If target UUID (--target-uuid) is not provided, target node UUID
    defaults to the user's inbox folder UUID. In other words, import will
    upload all documents to the user's inbox - if you want to change that, you
    need to provide UUID of the folder where you want to upload
    documents to.
    """
    host=ctx.obj['HOST']
    token = ctx.obj['TOKEN']
    perform_import(
        host=host,
        token=token,
        file_or_folder=file_or_folder,
        delete_after_upload=delete,
        parent_uuid=target_uuid
    )


@click.command(name="list")
@click.option(
    '--parent-uuid',
    help='Parent folder UUID'
)
@click.option(
    '--inbox',
    help='List nodes from Inbox folder',
    is_flag=True
)
@click.option(
    '--page-number',
    help='Page number to list',
    default=1
)
@click.option(
    '--page-size',
    help='Page size',
    default=15
)
@click.pass_context
def _list(ctx, parent_uuid, inbox, page_number, page_size):
    """Lists documents and folders of the given node

    If in case no specific node is requested - will list content
    of the user's home folder.
    """
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    perform_list(
        host=host,
        token=token,
        inbox=inbox,
        parent_uuid=parent_uuid,
        page_number=page_number,
        page_size=page_size
    )


@click.command(name="me")
@click.pass_context
def current_user(
    ctx
):
    """Show details of current user"""
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    perform_me(
        host=host,
        token=token,
    )


@click.command
@click.option(
    '--section',
    help='Limit output to preferences from this section only',
)
@click.option(
    '--name',
    help='Limit output to preferences with this only',
)
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
@click.option(
    '--section',
    help='Section name of the preference to update',
)
@click.option(
    '--name',
    help='Name of the preference to update',
)
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
@click.option(
    '-q',
    '--query',
    help='Text to search for',
)
@click.option(
    '-t',
    '--tags',
    help='Comma separated list of tags',
)
@click.option(
    '--tags-op',
    help='Should node contain all or any of the provided tags?',
    type=click.Choice(['all', 'any']),
    default='all',
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
    '-u',
    '--uuid',
    help='UUID of the node to download. You can use this option multiple times',
    type=click.UUID,
    multiple=True
)
@click.option(
    '-f',
    '--file-name',
    help='Name of the file where to save downloaded document/folder',
)
@click.option(
    '-t',
    '--archive-type',
    help='Download node as tar.gz or as .zip',
    type=click.Choice(['zip', 'targz']),
    default='zip',
    show_default=True
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


cli.add_command(auth)
cli.add_command(_import)
cli.add_command(_list)  # list nodes
cli.add_command(current_user)
cli.add_command(pref_list)
cli.add_command(pref_update)
cli.add_command(search)
cli.add_command(download)