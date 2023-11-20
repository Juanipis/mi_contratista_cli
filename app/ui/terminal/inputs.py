from datetime import datetime
from rich.console import Console
from prompt_toolkit import prompt
from app.ui.terminal.validators import get_valid_date


def get_date(console: Console, msg: str, date_format="%Y-%m-%d %H:%M:%S") -> datetime:
    while True:
        time_input = prompt(msg)
        time_input_parsed = get_valid_date(time_input, date_format)
        if time_input_parsed[1]:
            break
        else:
            console.print(
                "[bold red]Formato de fecha incorrecto. Intente nuevamente.[/bold red]"
            )

    return time_input_parsed[0]


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


def check_integer(console: Console, task_id: int) -> int:
    try:
        task_id = int(task_id)
        return task_id
    except ValueError:
        console.print("[bold red]Error: El ID debe ser un número.[/bold red]")
        return -1


def check_float(console: Console, number: float) -> float:
    try:
        number = float(number)
        return number
    except ValueError:
        console.print("[bold red]Error: El número debe ser un número.[/bold red]")
        return -1
