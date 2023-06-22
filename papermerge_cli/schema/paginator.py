from typing import TypeVar, Generic
from pydantic.generics import GenericModel

from collections.abc import Sequence

T = TypeVar('T')


class Paginator(GenericModel, Generic[T]):
    per_page: int
    page_number: int
    num_pages: int
    items: Sequence[T]
