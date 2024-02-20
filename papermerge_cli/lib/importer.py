import os
from pathlib import Path

from rich.console import Console

from papermerge_cli.rest import create_folder, get_me, upload_document
from papermerge_cli.schema import Folder, User

console = Console()


def upload_file_or_folder(
    host: str,
    token: str,
    file_or_folder: Path,
    parent_id=None,
    delete: bool = False
) -> None:
    user: User = get_me(host=host, token=token)

    # by default, upload will be uploded to the user home folder
    if parent_id is None:
        parent_id = user.inbox_folder_id

    if file_or_folder.is_file():
        upload_document(
            host=host,
            token=token,
            file_path=file_or_folder,
            parent_id=parent_id
        )
        if delete:
            remove(file_or_folder)

        return

    for entry in os.scandir(file_or_folder):
        if entry.is_file():
            upload_document(
                host=host,
                token=token,
                file_path=Path(entry.path),
                parent_id=parent_id
            )

            if delete:
                remove(Path(entry.path))
        else:
            folder_title = Path(entry.path).name

            folder: Folder = create_folder(
                host=host,
                token=token,
                title=folder_title,
                parent_id=parent_id
            )
            upload_file_or_folder(
                host=host,
                token=token,
                parent_id=folder.id,
                file_or_folder=Path(entry.path),
                delete=delete
            )
            if delete:
                remove(Path(entry.path))


def remove(path: Path):
    try:
        if path.is_file():
            os.remove(path)
        else:
            os.rmdir(path)
    except IOError:
        console.print(f"Error while removing {path}", style="red")
