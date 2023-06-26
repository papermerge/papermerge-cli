from laconiq import make

from papermerge_cli.lib.nodes import list_nodes
from papermerge_cli.schema import Node, Paginator, User


def titles_generator(items):
    for item in items:
        yield item


def test_list_nodes_returns_only_folders(requests_mock):
    """
    In this scenario GET /api/nodes/{node_id} returns
    a list of 3 folders i.e. all with ctype='folder'
    and with document field set to None.
    """
    user_me_url = 'http://test/api/users/me'
    user = make(User)
    requests_mock.get(
        user_me_url,
        text=user.json()
    )

    # URL to above-mentioned user's home folder
    params = 'page_number=1&per_page=15'
    home_id = 'a82cbe8e-fa0e-4aec-8950-7fcbeaef186c'
    nodes_url = f'http://test/api/nodes/{home_id}?{params}'

    folder_items = make(
        Node,
        _quantity=3,
        ctype="folder",
        title=titles_generator(["A1", "A2", "B1"]),
        document=None,
        user_id=str(user.id)
    )

    text_payload = make(
        Paginator,
        page_number=1,
        items=folder_items
    ).json()

    requests_mock.get(nodes_url, text=text_payload)

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
    user = make(User)

    requests_mock.get(
        user_me_url,
        text=user.json()
    )

    # URL to above-mentioned user's home folder
    params = 'page_number=1&per_page=15'
    home_id = user.home_folder_id
    nodes_url = f'http://test/api/nodes/{home_id}?{params}'

    node = make(
        Node,
        ctype="document",
        title="brother_004813.pdf",
        document={
            "ocr": True,
            "ocr_status": "SUCCESS"
        },
        user_id=str(user.id)
    )

    text_payload = make(
        Paginator,
        page_number=1,
        items=[node]
    ).json()

    requests_mock.get(nodes_url, text=text_payload)

    data: Paginator[Node] = list_nodes(
        host="http://test",
        token="abc",
        parent_uuid=home_id
    )

    assert data.page_number == 1
    assert len(data.items) == 1
    assert data.items[0].title == 'brother_004813.pdf'
