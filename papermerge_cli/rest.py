import papermerge_restapi_client
from pprint import pprint
from papermerge_restapi_client.apis.tags import auth_api
from papermerge_restapi_client.model.auth_token import AuthToken


def perform_auth(host, username, password):
    configuration = papermerge_restapi_client.Configuration(host=host)

    # Enter a context with an instance of the API client
    with papermerge_restapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = auth_api.AuthApi(api_client)
        auth_token = AuthToken(
            username=username,
            password=password,
        )

    try:
        api_response = api_instance.auth_login_create(auth_token)
        pprint(api_response)
    except papermerge_restapi_client.ApiException as e:
        print("Exception when calling AuthApi->auth_login_create: %s\n" % e)
