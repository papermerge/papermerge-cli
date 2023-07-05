from rich.table import Table

from papermerge_cli.schema import Node, Paginator


def list_nodes(data: Paginator[Node]) -> Table:
    table = Table(
        title=f"Page={data.page_number} of {data.num_pages}"
    )
    table.add_column("Type")
    table.add_column("Title")
    table.add_column("UUID", no_wrap=True)
    table.add_column("Tags")

    for node in data.items:
        table.add_row(
            node.ctype,
            node.title,
            str(node.id),
            ','.join(sorted(tag.name for tag in node.tags))
        )

    return table
