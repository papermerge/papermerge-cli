import uuid

from papermerge_cli.types import User
from papermerge_cli.api_client import ApiClient


def test_fetch_user(requests_mock):
    api_client = ApiClient(token='abc1', host='http://test')

    requests_mock.get('http://test/api/users/me', json={
        'id': 'ae86d82a-c8c5-4249-9d83-f722797edb8b',
        'email': 'john@mail.com',
        'username': 'john',
        'created_at': '2023-05-01T08:00Z',
        'updated_at': '2023-05-01T08:00Z',
        'home_folder_id': 'a82cbe8e-fa0e-4aec-8950-7fcbeaef186c',
        'inbox_folder_id': '3ad82662-7a69-4b8e-b7b3-06dababa6001'

    })
    json_response = api_client.get('/api/users/me')
    u = User(**json_response)

    assert u.email == 'john@mail.com'
    assert u.home_folder_id == uuid.UUID('a82cbe8e-fa0e-4aec-8950-7fcbeaef186c')
