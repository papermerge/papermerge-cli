from enum import Enum
from typing import TypeVar

DocumentVersion = TypeVar("DocumentVersion")


class OCRStatusEnum(str, Enum):
    unknown = 'UNKNOWN'
    received = 'RECEIVED'
    started = 'STARTED'
    success = 'SUCCESS'
    failed = 'FAILED'


class NodeActionEnum(str, Enum):
    add_tags = "add-tags"
    append_tags = "append-tags"  # same as "add-tags"
    assign_tags = "assign-tags"
    replace_tags = "replace-tags"  # same as "assign-tags"
    remove_tags = "remove-tags"
    delete_tags = "delete-tags"   # same as "remove-tags"
