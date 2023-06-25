from papermerge_cli.rest.documents import upload as upload_document


def test_upload_document(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "invoice.pdf"
    file_path.write_bytes(b'invoice binary content')

    upload_document(
        host="http://test",
        token="abc",
        file_path=file_path
    )
