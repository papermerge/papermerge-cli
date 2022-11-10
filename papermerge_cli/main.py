import os
import click

from .rest import perform_auth, perform_list, perform_me

PREFIX = 'PAPERMERGE_CLI'


@click.group()
@click.pass_context
@click.option(
    '--host',
    default=lambda: os.environ.get('HOST', None),
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
def cli(ctx, host, token):
    ctx.ensure_object(dict)
    ctx.obj['HOST'] = host
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
    confirmation_prompt=True,
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
def _import():
    """Import documents from local folder"""
    click.echo('import')


@click.command(name="list")
@click.option(
    '--parent-uuid',
    help='Parent folder UUID'
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
def _list(ctx, parent_uuid, page_number, page_size):
    """Lists documents and folders"""
    token = ctx.obj['TOKEN']
    host = ctx.obj['HOST']
    perform_list(
        host=host,
        token=token,
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


cli.add_command(auth)
cli.add_command(_import)
cli.add_command(_list)
cli.add_command(current_user)
