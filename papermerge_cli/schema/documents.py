from datetime import datetime
from typing import Literal, Tuple
from uuid import UUID

from pydantic import BaseModel

from papermerge_cli.types import OCRStatusEnum


class CreateDocument(BaseModel):
    title: str
    ctype: Literal["document"] = "document"
    parent_id: UUID | None
    lang: str | None = None
    file_name: str | None = None


class Page(BaseModel):
    id: UUID
    number: int
    text: str = ''
    lang: str
    document_version_id: UUID
    svg_url: str | None
    jpg_url: str | None


class DocumentVersion(BaseModel):
    id: UUID
    number: int
    lang: str
    file_name: str | None = None
    size: int = 0
    page_count: int = 0
    short_description: str
    document_id: UUID
    download_url: str | None = None
    pages: list[Page] = []


class Document(BaseModel):
    id: UUID
    title: str
    ctype: Literal["document"]
    created_at: datetime
    updated_at: datetime
    parent_id: UUID | None
    user_id: UUID
    breadcrumb: list[Tuple[UUID, str]]
    versions: list[DocumentVersion] = []
    ocr: bool = True  # will this document be OCRed?
    ocr_status: OCRStatusEnum = OCRStatusEnum.unknown
