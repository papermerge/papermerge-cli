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
        if response.status_code != 200:
            raise ValueError(response.text)

        return response_model(**response.json())

    def post(
        self,
        url,
        json,
        response_model=None
    ):
        response = requests.post(
            f"{self.host}{url}",
            headers=self.headers,
            json=json
        )

        if response.status_code not in (200, 201):
            raise ValueError(response.text)

        if response_model:
            return response_model(**response.json())

    def patch(
        self,
        url,
        json,
        response_model=None
    ):
        response = requests.patch(
            f"{self.host}{url}",
            headers=self.headers,
            json=json
        )

        if response.status_code not in (200, 201):
            raise ValueError(response.text)

        if response_model:
            return response_model(**response.json())

    def delete(
        self,
        url,
        json,
    ):
        requests.delete(
            f"{self.host}{url}",
            headers=self.headers,
            json=json
        )

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
