from pathlib import Path
from uuid import UUID

from papermerge_cli.api_client import ApiClient
from papermerge_cli.schema import CreateDocument, Document


def upload(
    host: str,
    token: str,
    file_path: Path,
    parent_id: UUID
) -> Document:
    api_client = ApiClient[Document](token=token, host=host)

    doc_to_create = CreateDocument(
        title=file_path.name,
        file_name=file_path.name,
        parent_id=parent_id
    )

    response_doc: Document = api_client.post(
        '/api/nodes/',
        response_model=Document,
        json=doc_to_create.model_dump(mode='json')
    )

    result_doc: Document = api_client.upload(
        f'/api/documents/{response_doc.id}/upload',
        file_path,
        response_model=Document
    )

    return result_doc
