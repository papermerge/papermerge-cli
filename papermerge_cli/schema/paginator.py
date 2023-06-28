from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar('T')


class Paginator(GenericModel, Generic[T]):
    page_size: int
    page_number: int
    num_pages: int
    items: Sequence[T]
