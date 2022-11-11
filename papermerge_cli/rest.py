import os
import click
import papermerge_restapi_client

from papermerge_restapi_client.apis.tags import (
    auth_api,
    users_api,
    nodes_api,
    documents_api
)
from papermerge_restapi_client.model.auth_token_request import AuthTokenRequest


def get_restapi_client(host, token):
    configuration = papermerge_restapi_client.Configuration(host=host)
    configuration.api_key['Token Authentication'] = f'Token {token}'

    return papermerge_restapi_client.ApiClient(configuration)


def get_user_home_uuid(restapi_client):
    api_instance = users_api.UsersApi(restapi_client)

    resp = api_instance.users_me_retrieve()
    ret = resp.body['data']['relationships']['home_folder']['data']['id']

    return ret


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
    documents_api_instance.upload_file(
        body=body,
        path_params=path_params
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


def perform_import(host, token, file_or_folder):

    restapi_client = get_restapi_client(host, token)
    home_uuid = get_user_home_uuid(restapi_client)

    if os.path.isfile(file_or_folder):
        click.echo(f"Importing {file_or_folder}...")
        upload_document(
            restapi_client=restapi_client,
            parent_uuid=home_uuid,
            file_path=file_or_folder
        )
        return

    for entry in os.scandir(file_or_folder):
        if entry.is_file():
            click.echo(f"Importing {entry.path}...")
            upload_document(
                restapi_client=restapi_client,
                parent_uuid=home_uuid,
                file_path=entry.path
            )
        else:
            click.echo(f"Skipping {entry.path} as it is not a file")
