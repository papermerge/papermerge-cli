from pathlib import Path

from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema import CreateDocument, Document


def upload(
    host: str,
    token: str,
    file_path: Path,
    parent_uuid=None,
) -> None:
    api_client = ApiClient[Document](token=token, host=host)
    doc_to_create = CreateDocument(
        title=file_path.name,
        file_name=file_path.name,
        parent_id=parent_uuid
    )

    doc: Document = api_client.post(
        '/api/nodes/',
        json=doc_to_create.json()
    )

    api_client.upload(
        f'/api/documents/{doc.id}/upload',
        file_path
    )
