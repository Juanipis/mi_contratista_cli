from rich.table import Table


def create_task_table() -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Start Time")
    table.add_column("End Time")
    table.add_column("Description")
    return table
