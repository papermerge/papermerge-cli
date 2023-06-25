from typing import Generic, TypeVar

import requests

T = TypeVar('T')


class ApiClient(Generic[T]):

    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token

    def get(
        self,
        url: str,
        response_model=T,
        query_params=None
    ) -> T:
        response = requests.get(
            f"{self.host}{url}",
            headers=self.headers,
            params=query_params
        )
        return response_model(**response.json())

    def post(
        self,
        url,
        json,
        response_model=T
    ):
        response = requests.post(
            f"{self.host}{url}",
            headers=self.headers,
            json=json
        )
        return response_model(**response.json())

    @property
    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.token}'}
