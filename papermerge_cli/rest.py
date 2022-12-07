import os
import click
import papermerge_restapi_client

from papermerge_restapi_client.apis.tags import (
    auth_api,
    users_api,
    nodes_api,
    documents_api,
    preferences_api,
    search_api
)
from papermerge_restapi_client.model.auth_token_request import AuthTokenRequest

from .utils import pretty_breadcrumb

def get_restapi_client(host, token):
    configuration = papermerge_restapi_client.Configuration(host=host)
    configuration.api_key['Token Authentication'] = f'Token {token}'

    return papermerge_restapi_client.ApiClient(configuration)


def get_user_home_uuid(restapi_client):
    api_instance = users_api.UsersApi(restapi_client)

    resp = api_instance.users_me_retrieve()
    ret = resp.body['data']['relationships']['home_folder']['data']['id']

    return ret


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

    click.echo(f'user_uuid={user_uuid}')
    click.echo(f'username={username}')
    click.echo(f'email={email}')
    click.echo(f'home folder uuid={home_folder_uuid}')
    click.echo(f'inbox folder uuid={inbox_folder_uuid}')


def perform_import(host: str, token: str, file_or_folder: str, parent_uuid=None) -> None:
    """Performs recursive import of given path"""
    restapi_client = get_restapi_client(host, token)
    if parent_uuid is None:
        parent_uuid = get_user_home_uuid(restapi_client)

    if os.path.isfile(file_or_folder):
        # if file_or_folder is a path to document (i.e. file),then just
        # upload that document and we are done!
        click.echo(f"Importing {file_or_folder}")
        upload_document(
            restapi_client=restapi_client,
            parent_uuid=parent_uuid,
            file_path=file_or_folder
        )
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
                parent_uuid=folder_uuid
            )


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
