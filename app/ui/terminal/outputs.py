import time
import arrow
from rich.console import Console
from app.models.task import Task
from app.ui.terminal.table import create_task_table


def show_one_task(console: Console, task: Task):
    table = create_task_table()
    table.add_row(
        str(task.id),
        task.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        task.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        task.description,
    )

    console.print(table)


def show_options(console: Console):
    console.print("[bold magenta]Opciones disponibles:[/bold magenta]")
    options = [
        "Iniciar una nueva tarea",
        "Generar un reporte",
        "Insertar tarea manualmente",
        "Mostrar las tareas",
        "Eliminar tarea por ID",
        "Resetear las tareas",
        "Salir",
    ]
    for i, option in enumerate(options, start=1):
        console.print(f"[bold cyan]{i}.[/bold cyan] {option}")


def timer(console: Console, start_time: arrow.Arrow):
    try:
        with console.status("[bold green]Tarea en curso...[/bold green]") as status:
            while True:
                elapsed = arrow.now() - start_time
                status.update(f"Tiempo transcurrido: [bold]{str(elapsed)}[/bold]")
                time.sleep(1)
    except KeyboardInterrupt:
        pass


def show_tasks_table(console: Console, tasks: list[Task]):
    table = create_task_table()
    for task in tasks:
        table.add_row(
            str(task.id),
            task.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            task.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            task.description,
        )
    console.print(table)
