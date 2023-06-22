from rich.table import Table

from papermerge_cli.schema.users import User


def current_user(user: User) -> Table:
    table = Table(
        title=f"Current User (username={user.username}/email={user.email})"
    )

    table.add_column("User/UUID", no_wrap=True)
    table.add_column("Home/UUID", no_wrap=True)
    table.add_column("Inbox/UUID", no_wrap=True)

    table.add_row(
        str(user.id),
        str(user.home_folder_id),
        str(user.inbox_folder_id)
    )

    return table
