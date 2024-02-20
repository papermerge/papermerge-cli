from uuid import UUID

from laconiq import make

from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema.users import User


def test_fetch_user(requests_mock):
    api_client = ApiClient[User](token='abc1', host='http://test')

    user = make(
        User,
        email='john@mail.com',
        home_folder_id=UUID('a82cbe8e-fa0e-4aec-8950-7fcbeaef186c')
    )
    requests_mock.get('http://test/api/users/me', text=user.model_dump_json())
    got_user = api_client.get('/api/users/me', response_model=User)

    assert got_user.email == 'john@mail.com'
    expected_uuid = UUID('a82cbe8e-fa0e-4aec-8950-7fcbeaef186c')
    assert got_user.home_folder_id == expected_uuid
