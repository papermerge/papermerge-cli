import click
import papermerge_restapi_client
from papermerge_restapi_client.apis.tags import (
    auth_api,
    users_api,
    nodes_api
)
from papermerge_restapi_client.model.auth_token_request import AuthTokenRequest


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


def perform_list(host, token, parent_uuid=None):
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
    click.echo(f'user_uuid={user_uuid}')
    click.echo(f'home folder uuid={home_folder_uuid}')
    click.echo(f'inbox folder uuid={inbox_folder_uuid}')


    with papermerge_restapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = nodes_api.NodesApi(api_client)

    if parent_uuid is None:
        path_params = {
            'id': home_folder_uuid,
        }
    else:
        path_params = {
            'id': parent_uuid
        }

    response = api_instance.retrieve_node(path_params=path_params)

    click.echo(response)