import os
import click
import backoff
import papermerge_restapi_client
from rich.console import Console
from rich.table import Table

from papermerge_restapi_client.apis.tags import (
    auth_api,
    users_api,
    nodes_api,
    documents_api,
    preferences_api,
    search_api
)
from papermerge_restapi_client.model.auth_token_request import AuthTokenRequest

from .utils import pretty_breadcrumb, auth_required


console = Console()


def backoff_giveup_condition(
    exception: papermerge_restapi_client.exceptions.ApiException
) -> bool:
    """
    Decides if it is the case to retry the REST API call
    :param exception: exception raised by REST API client
    :return: True - means - do not retry i.e. give up
        False - means - please retry the REST API call

    This method is designed to be used only as argument
    to the decorator `backoff.on_exception`
    """

    # Will retry only of REST API exception had status 502 i.e. bad gateway
    should_retry = exception.status > 500

    if should_retry:
        click.echo("Retrying...")

    # Should not retry.
    # If True -> do not try anymore i.e. give up
    return not should_retry


def get_restapi_client(host, token):
    configuration = papermerge_restapi_client.Configuration(host=host)
    configuration.api_key['Token Authentication'] = f'Token {token}'

    return papermerge_restapi_client.ApiClient(configuration)


@auth_required
def get_user_home_uuid(restapi_client):
    api_instance = users_api.UsersApi(restapi_client)

    resp = api_instance.users_me_retrieve()
    ret = resp.body['data']['relationships']['home_folder']['data']['id']

    return ret


@auth_required
def get_user_inbox_uuid(restapi_client):
    api_instance = users_api.UsersApi(restapi_client)

    resp = api_instance.users_me_retrieve()
    ret = resp.body['data']['relationships']['inbox_folder']['data']['id']

    return ret

@auth_required
@backoff.on_exception(
    backoff.expo,
    papermerge_restapi_client.exceptions.ApiException,
    max_tries=10,
    giveup=backoff_giveup_condition
)
def create_folder(
    restapi_client,
    parent_uuid: str,
    title: str
) -> str:
    nodes_api_instance = nodes_api.NodesCreate(restapi_client)

    body = dict(
        data=dict(
            type="folders",
            attributes=dict(
                title=title,
            ),
            relationships=dict(
                parent=dict(
                    data=dict(
                        type="folders",
                        id=parent_uuid,
                    ),
                ),
            ),
        ),
    )
    response = nodes_api_instance.nodes_create(body=body)
    folder_uuid = response.body['data']['id']

    return folder_uuid

@auth_required
@backoff.on_exception(
    backoff.expo,
    papermerge_restapi_client.exceptions.ApiException,
    max_tries=10,
    giveup=backoff_giveup_condition
)
def upload_document(restapi_client, parent_uuid, file_path):
    nodes_api_instance = nodes_api.NodesCreate(restapi_client)
    title = os.path.basename(file_path)

    body = dict(
        data=dict(
            type="documents",
            attributes=dict(
                title=title,
            ),
            relationships=dict(
                parent=dict(
                    data=dict(
                        type="folders",
                        id=parent_uuid,
                    ),
                ),
            ),
        ),
    )
    response = nodes_api_instance.nodes_create(body=body)
    document_uuid = response.body['data']['id']
    documents_api_instance = documents_api.UploadFile(restapi_client)

    with open(file_path, 'rb') as f:
        body = f.read()

    path_params = {
        'file_name': title,
        'document_id': document_uuid
    }
    header_params = {
        'Content-Disposition': f'attachment; filename={title}'
    }
    documents_api_instance.upload_file(
        body=body,
        path_params=path_params,
        header_params=header_params,
        skip_deserialization=True
    )


def perform_auth(host, username, password):
    configuration = papermerge_restapi_client.Configuration(host=host)

    # Enter a context with an instance of the API client
    with papermerge_restapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = auth_api.AuthApi(api_client)
        auth_body = AuthTokenRequest(
            username=username,
            password=password,
        )

    api_response = api_instance.auth_login_create(auth_body)
    return api_response.body['token']

@auth_required
def perform_list(
    host,
    token,
    parent_uuid=None,
    page_number=1,
    page_size=15
):
    configuration = papermerge_restapi_client.Configuration(host=host)
    configuration.api_key['Token Authentication'] = f'Token {token}'

    # Enter a context with an instance of the API client
    with papermerge_restapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = users_api.UsersApi(api_client)

    response = api_instance.users_me_retrieve()

    user_uuid = response.body['data']['id']
    home_folder_uuid = \
        response.body['data']['relationships']['home_folder']['data']['id']
    inbox_folder_uuid = \
        response.body['data']['relationships']['inbox_folder']['data']['id']

    with papermerge_restapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        nodes_api_instance = nodes_api.NodesApi(api_client)

    if parent_uuid is None:
        path_params = {
            'id': home_folder_uuid,
        }
    else:
        path_params = {
            'id': parent_uuid
        }

    query_params = {
        'page[number]': page_number,
        'page[size]': page_size
    }

    response = nodes_api_instance.node_retrieve(
        path_params=path_params,
        query_params=query_params
    )

    page = response.body['meta']['pagination']['page']
    pages = response.body['meta']['pagination']['pages']
    count = response.body['meta']['pagination']['count']
    click.echo(f"Page={page} of {pages}. Total nodes={count}")

    for node in response.body['data']:
        type_letter = 'd' if node['type'] == 'Document' else 'f'
        title = node['attributes']['title']
        uuid = node['id']
        click.echo(f"{type_letter} {title} {uuid}")


@auth_required
def perform_me(
    host,
    token
):
    configuration = papermerge_restapi_client.Configuration(host=host)
    configuration.api_key['Token Authentication'] = f'Token {token}'

    # Enter a context with an instance of the API client
    with papermerge_restapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = users_api.UsersApi(api_client)

    response = api_instance.users_me_retrieve()

    user_uuid = response.body['data']['id']
    username = response.body['data']['attributes']['username']
    email = response.body['data']['attributes']['email']
    home_folder_uuid = \
        response.body['data']['relationships']['home_folder']['data']['id']
    inbox_folder_uuid = \
        response.body['data']['relationships']['inbox_folder']['data']['id']

    table = Table(
        title=f"Current User (username={username}/email={email})"
    )

    table.add_column("User/UUID", no_wrap=True)
    table.add_column("Home/UUID", no_wrap=True)
    table.add_column("Inbox/UUID", no_wrap=True)

    table.add_row(
        user_uuid,
        home_folder_uuid,
        inbox_folder_uuid
    )
    console.print(table)


@auth_required
def perform_import(
    host: str,
    token: str,
    file_or_folder: str,
    parent_uuid=None,
    delete_after_upload: bool=False
) -> None:
    """Performs recursive import of given path"""
    restapi_client = get_restapi_client(host, token)
    if parent_uuid is None:
        parent_uuid = get_user_inbox_uuid(restapi_client)

    if os.path.isfile(file_or_folder):
        # if file_or_folder is a path to document (i.e. file),then just
        # upload that document and we are done!
        click.echo(f"Importing {file_or_folder}")
        upload_document(
            restapi_client=restapi_client,
            parent_uuid=parent_uuid,
            file_path=file_or_folder
        )
        if delete_after_upload:
            os.remove(file_or_folder)
        return

    # If we are here, this means that file_or_folder is actually a path to
    # folder
    for entry in os.scandir(file_or_folder):
        if entry.is_file():
            click.echo(f"Importing {entry.path}")
            upload_document(
                restapi_client=restapi_client,
                parent_uuid=parent_uuid,
                file_path=entry.path
            )
            if delete_after_upload:
                os.remove(entry.path)
        else:
            folder_title = os.path.basename(entry.path)
            folder_uuid = create_folder(
                restapi_client,
                parent_uuid=parent_uuid,
                title=folder_title,
            )
            perform_import(
                host=host,
                token=token,
                file_or_folder=entry.path,
                parent_uuid=folder_uuid,
                delete_after_upload=delete_after_upload
            )
            if delete_after_upload:
                os.rmdir(entry.path)

@auth_required
def perform_pref_list(
    host: str,
    token: str,
    section: str | None = None,
    name: str | None = None
) -> None:
    """Shows preferences of the user identified by token"""
    restapi_client = get_restapi_client(host, token)
    api_instance = preferences_api.PreferencesApi(restapi_client)
    response = api_instance.preferences_list()

    for item in response.body['data']:
        pref = item['attributes']
        _sec = pref['section']
        _name = pref['name']
        value = pref['value']
        if (section is None or section == _sec) and (name is None or _name == name):
            click.echo(f"section={_sec} name={_name} value={value}")

@auth_required
def perform_pref_update(
    host: str,
    token: str,
    section: str,
    name: str,
    value: str
) -> None:
    """Update given preference identified by section and name"""
    restapi_client = get_restapi_client(host, token)
    api_instance = preferences_api.PreferencesApi(restapi_client)

    body = dict()
    body[f"{section}__{name}"] = value

    api_instance.preferences_bulk_create(
        body=body,
        skip_deserialization=True,
        content_type='application/json'
    )
    click.echo(f"'{section}__{name}' successfully set to '{value}'")


@auth_required
def perform_search(
    host: str,
    token: str,
    query: str,
    tags: str,
    tags_op: str
) -> None:

    restapi_client = get_restapi_client(host, token)
    api_instance = search_api.SearchApi(restapi_client)

    query_params = dict(tags_op=tags_op)

    if query is not None:
        query_params['q'] = query
    if tags is not None:
        query_params['tags'] = tags

    response = api_instance.search(
        query_params=query_params
    )

    for item in response.body:
        if item['node_type'] in ('document'):
            ntype = 'd'
        else:
            ntype = 'f'

        breadcrumb = pretty_breadcrumb(item['breadcrumb'])
        click.echo(
            f"{ntype}\t{item['title']}\t{item['id']}\t{breadcrumb}"
            f"\t{item['tags']}"
        )

@auth_required
def perform_download(
    host: str,
    token: str,
    uuids: tuple[click.UUID],
    archive_type: str,
    file_name: str = None,
) -> None:

    restapi_client = get_restapi_client(host, token)
    api_instance = nodes_api.NodesDownload(restapi_client)
    query_params = {
        'node_ids': uuids,
        'archive_type': archive_type
    }

    response = api_instance.nodes_download(
        query_params=query_params,
        accept_content_types=(
            '*/*',
        ),
        skip_deserialization=True
    )
    if file_name is None:
        _file_name = 'default'

        for key, value in response.response.headers.items():
            if 'content-disposition' in key.lower():
                # value example = 'attachment; filename=brother_004309.pdf'
                # from the value we need file name
                _file_name = value.split(';')[1].split('=')[1]

        file_name = _file_name

    with open(file_name, 'wb') as f:
        f.write(response.response.data)

    click.echo(f"Downloaded to {file_name}")
