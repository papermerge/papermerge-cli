

def test_upload_document(tmp_path, requests_mock):
    """
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "invoice.pdf"
    file_path.write_bytes(b'invoice binary content')

    user = make(User)
    user_me_url = 'http://test/api/users/me'
    requests_mock.get(
        user_me_url,
        text=user.json()
    )
    nodes_url = 'http://test/api/nodes'
    requests_mock.post(
        nodes_url,
        data=make(CreateDocument).json(),
        text=make(Document, user_id=str(user.id)).json()
    )

    upload_document(
        host="http://test",
        token="abc",
        file_path=file_path
    )
    """
