from uuid import UUID

from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema.users import User


def test_fetch_user(requests_mock):
    api_client = ApiClient[User](token='abc1', host='http://test')

    requests_mock.get('http://test/api/users/me', json={
        'id': 'ae86d82a-c8c5-4249-9d83-f722797edb8b',
        'email': 'john@mail.com',
        'username': 'john',
        'created_at': '2023-05-01T08:00Z',
        'updated_at': '2023-05-01T08:00Z',
        'home_folder_id': 'a82cbe8e-fa0e-4aec-8950-7fcbeaef186c',
        'inbox_folder_id': '3ad82662-7a69-4b8e-b7b3-06dababa6001'

    })
    user = api_client.get('/api/users/me', response_modal=User)

    assert user.email == 'john@mail.com'
    assert user.home_folder_id == UUID('a82cbe8e-fa0e-4aec-8950-7fcbeaef186c')
