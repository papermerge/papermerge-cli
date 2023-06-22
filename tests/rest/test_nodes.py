from papermerge_cli.schema import Node, Paginator

from papermerge_cli.rest.nodes import list_nodes


def test_list_nodes_returns_only_folders(requests_mock):
    """
    In this scenario GET /api/nodes/{node_id} returns
    a list of 3 folders i.e. all with ctype='folder'
    and with document field set to None.
    """
    user_me_url = 'http://test/api/users/me'
    requests_mock.get(
        user_me_url,
        json={
            'id': 'ae86d82a-c8c5-4249-9d83-f722797edb8b',
            'email': 'john@mail.com',
            'username': 'john',
            'created_at': '2023-05-01T08:00Z',
            'updated_at': '2023-05-01T08:00Z',
            'home_folder_id': 'a82cbe8e-fa0e-4aec-8950-7fcbeaef186c',
            'inbox_folder_id': '3ad82662-7a69-4b8e-b7b3-06dababa6001'

        }
    )

    # URL to above-mentioned user's home folder
    params = 'page_number=1&per_page=15'
    home_id = 'a82cbe8e-fa0e-4aec-8950-7fcbeaef186c'
    nodes_url = f'http://test/api/nodes/{home_id}?{params}'

    requests_mock.get(nodes_url, json={
        'num_pages': 1,
        'page_number': 1,
        'per_page': 5,
        'items': [
          {
            "id": "be378c95-7c6f-4aba-9019-ae1fd5fe56cd",
            "title": "A1",
            "ctype": "folder",
            "created_at": "2023-06-18T11:21:46.893912+00:00",
            "updated_at": "2023-06-18T11:21:46.893960+00:00",
            "parent_id": "b23498b2-c1b2-401a-93b6-eb5130f9cd91",
            "user_id": "bd1b4f6a-bdd0-4a46-a26d-98e0b7e5f3c1",
            "document": None
          },
          {
            "id": "bb8c8007-d7b0-43be-b55a-edc13ee9f9d1",
            "title": "A2",
            "ctype": "folder",
            "created_at": "2023-06-18T11:33:23.930819+00:00",
            "updated_at": "2023-06-18T11:33:23.930870+00:00",
            "parent_id": "b23498b2-c1b2-401a-93b6-eb5130f9cd91",
            "user_id": "bd1b4f6a-bdd0-4a46-a26d-98e0b7e5f3c1",
            "document": None
          },
          {
            "id": "185296e6-5893-48af-b75c-b2e10aae39ab",
            "title": "B1",
            "ctype": "folder",
            "created_at": "2023-06-19T04:30:31.989652+00:00",
            "updated_at": "2023-06-19T04:30:31.989709+00:00",
            "parent_id": "b23498b2-c1b2-401a-93b6-eb5130f9cd91",
            "user_id": "bd1b4f6a-bdd0-4a46-a26d-98e0b7e5f3c1",
            "document": None
          }
        ]
    })

    data: Paginator[Node] = list_nodes(
        host="http://test",
        token="abc",
        parent_uuid=home_id
    )

    actual_titles = set([node.title for node in data.items])
    expected_titles = {'A1', 'A2', 'B1'}

    assert data.page_number == 1
    assert len(data.items) == 3
    assert actual_titles == expected_titles


def test_list_nodes_returns_one_ocred_document(requests_mock):
    """
    In this scenario GET /api/nodes/{node_id} returns
    one document which was OCRed.
    """
    user_me_url = 'http://test/api/users/me'
    requests_mock.get(
        user_me_url,
        json={
            'id': 'ae86d82a-c8c5-4249-9d83-f722797edb8b',
            'email': 'john@mail.com',
            'username': 'john',
            'created_at': '2023-05-01T08:00Z',
            'updated_at': '2023-05-01T08:00Z',
            'home_folder_id': 'a82cbe8e-fa0e-4aec-8950-7fcbeaef186c',
            'inbox_folder_id': '3ad82662-7a69-4b8e-b7b3-06dababa6001'
        }
    )

    # URL to above-mentioned user's home folder
    params = 'page_number=1&per_page=15'
    home_id = 'a82cbe8e-fa0e-4aec-8950-7fcbeaef186c'
    nodes_url = f'http://test/api/nodes/{home_id}?{params}'

    requests_mock.get(nodes_url, json={
        'num_pages': 1,
        'page_number': 1,
        'per_page': 5,
        'items': [
            {
                "id": "5f57c4b6-8601-45c1-9ff9-258da5ae0f85",
                "title": "brother_004813.pdf",
                "ctype": "document",
                "created_at": "2023-06-20T05:47:57.247718+00:00",
                "updated_at": "2023-06-20T05:47:59.790392+00:00",
                "parent_id": "1cd7e113-c46b-4413-ab8a-ca8cb0ec7e20",
                "user_id": "bd1b4f6a-bdd0-4a46-a26d-98e0b7e5f3c1",
                "document": {
                    "ocr": True,
                    "ocr_status": "SUCCESS"
                }
            }
        ]
    })

    data: Paginator[Node] = list_nodes(
        host="http://test",
        token="abc",
        parent_uuid=home_id
    )

    assert data.page_number == 1
    assert len(data.items) == 1
    assert data.items[0].title == 'brother_004813.pdf'
