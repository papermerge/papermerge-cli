import os
import click

from .rest import perform_auth

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
    click.echo(f"host={host} token={token}")
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
    perform_auth(
        host=ctx.obj['HOST'],
        username=username,
        password=password
    )


@click.command(name="import")
def _import():
    click.echo('import')


cli.add_command(auth)
cli.add_command(_import)
