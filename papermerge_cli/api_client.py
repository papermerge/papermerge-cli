import requests

from pydantic import BaseModel
from typing import Generic, TypeVar



T = TypeVar('T')

class ApiClient(Generic[T]):

    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token

    def get(
        self,
        url: str,
        response_modal=T,
        query_params=None
    ) -> T:
        response = requests.get(
            f"{self.host}{url}",
            headers=self.headers,
            params=query_params
        )
        return response_modal(**response.json())

    @property
    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.token}'}
