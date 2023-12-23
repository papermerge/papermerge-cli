from mimetypes import guess_type
from pathlib import Path
from typing import Generic, TypeVar

import requests

from papermerge_cli.exceptions import FileMimeTypeUnknown

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
        headers = {
            'Content-Type': 'application/json',
            **self.headers
        }
        response = requests.post(
            f"{self.host}{url}",
            headers=headers,
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
        mime_type, _ = guess_type(file_path)

        if mime_type is None:
            msg = f"{file_path} mime type cannot be guessed"
            raise FileMimeTypeUnknown(msg)

        data = open(file_path, 'rb').read()
        # https://stackoverflow.com/a/35974071/381116
        multipart_form_data = {
            'file': (file_path.name, data, mime_type),
        }
        response = requests.post(
            f"{self.host}{url}",
            headers=self.headers,
            files=multipart_form_data
        )

        if response.status_code != 200:
            raise ValueError(response.text)

        return response_model(**response.json())

    @property
    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.token}'}
