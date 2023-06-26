from pathlib import Path

from papermerge_cli.rest import get_me, upload_document
from papermerge_cli.schema import Document, User


def upload(
    host: str,
    token: str,
    file_path: Path,
    parent_id=None,
) -> Document:
    user: User = get_me(host=host, token=token)

    # by default, upload will be uploded to the user home folder
    if parent_id is None:
        parent_id = user.home_folder_id

    doc: Document = upload_document(
        host=host,
        token=token,
        file_path=file_path,
        parent_id=parent_id
    )

    return doc
