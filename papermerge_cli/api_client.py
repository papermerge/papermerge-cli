from pathlib import Path
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
        response_model,
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
        response_model
    ):
        response = requests.post(
            f"{self.host}{url}",
            headers=self.headers,
            data=json
        )

        if response.status_code != 201:
            raise ValueError(response.text)

        return response_model(**response.json())

    def upload(
        self,
        url: str,
        file_path: Path,
        response_model
    ) -> T:
        data = open(file_path, 'rb').read()
        response = requests.post(
            f"{self.host}{url}",
            headers=self.headers,
            files=dict(file=data)
        )
        if response.status_code != 200:
            raise ValueError(response.text)

        return response_model(**response.json())

    @property
    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.token}'}
