from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ValidationError, field_validator

from papermerge_cli.types import OCRStatusEnum


class NodeType(str, Enum):
    document = "document"
    folder = "folder"


class UpdateNode(BaseModel):
    title: Optional[str]
    parent_id: Optional[UUID]

    @field_validator('parent_id')
    def parent_id_is_not_none(cls, value):
        if value is None:
            raise ValidationError('Cannot set parent_id to None')
        return value


class DocumentNode(BaseModel):
    """Minimalist part of the document returned as part of nodes list"""
    ocr: bool = True  # will this document be OCRed?
    ocr_status: OCRStatusEnum = OCRStatusEnum.unknown


class Tag(BaseModel):
    name: str
    bg_color: str
    fg_color: str


class Node(BaseModel):
    id: UUID
    title: str
    ctype: NodeType
    tags: List[Tag]
    created_at: datetime
    updated_at: datetime
    parent_id: UUID | None = None
    user_id: UUID
    document: DocumentNode | None = None

    @field_validator('document', mode='before')
    def document_validator(cls, value, values):
        if values.data['ctype'] == NodeType.document:
            return DocumentNode(
                ocr_status=value['ocr_status'],
                ocr=value['ocr']
            )

        return None


class CreateNode(BaseModel):
    title: str
    ctype: NodeType.folder
    parent_id: UUID | None


class CreateDocumentNode(BaseModel):
    title: str
    ctype: NodeType.document
    parent_id: UUID | None


class MoveNode(BaseModel):
    source_ids: List[UUID]
    target_id: UUID
