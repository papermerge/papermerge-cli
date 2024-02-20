from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class Paginator(BaseModel, Generic[T]):
    page_size: int
    page_number: int
    num_pages: int
    items: Sequence[T]
