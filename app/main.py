from app.models.task import Task
from app.ui.terminal.outputs import show_one_task, show_options, timer, show_tasks_table
from app.usecase.task.task_manager import TaskManager
from app.usecase.report.report_generator import ReportGenerator
from rich.console import Console
from app.ui.terminal.inputs import get_date, check_integer, check_float
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm
import arrow


def main():
    manager = TaskManager()
    report_gen = ReportGenerator()
    console = Console()
    try:
        while True:
            show_options(console)

            option = prompt("Seleccione una opción: ")

            if option == "1":
                start_new_task(manager, console)

            elif option == "2":
                generate_report(report_gen, console)

            elif option == "3":
                insert_task_manually(manager, console)

            elif option == "4":
                show_tasks(manager, console)

            elif option == "5":
                delete_task_by_id(manager, console)

            elif option == "6":
                reset_tasks(manager, console)

            elif option == "7":
                console.print("[bold yellow]Saliendo...[/bold yellow]")
                manager.close()
                break
            else:
                console.print(
                    "[bold red]Opción inválida. Por favor, seleccione una opción válida.[/bold red]"
                )
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        console.print("[bold yellow]Saliendo...[/bold yellow]")
        manager.close()


def insert_task_manually(manager: TaskManager, console: Console):
    start_time = get_date(
        console, "Ingrese la fecha de inicio de la tarea (YYYY-MM-DD HH:MM:SS): "
    )
    end_time = get_date(
        console, "Ingrese la fecha de fin de la tarea (YYYY-MM-DD HH:MM:SS): "
    )
    description = prompt("Ingrese la descripción de la tarea: ")

    show_one_task(
        console,
        Task(id=0, start_time=start_time, end_time=end_time, description=description),
    )
    if not confirm("¿Desea guardar la tarea?"):
        return

    if manager.add_task_manually(start_time, end_time, description):
        console.print("[bold green]Tarea agregada.[/bold green]")
    else:
        console.print(
            "[bold red]Error al agregar tarea. Asegúrese de que la fecha de inicio sea menor que la fecha de fin.[/bold red]"
        )


def delete_task_by_id(manager: TaskManager, console: Console):
    task_id = prompt("Ingrese el ID de la tarea a eliminar: ")
    task_id = check_integer(console, task_id)
    if task_id == -1:
        console.print("[bold red]Error: El ID debe ser un número valido.[/bold red]")
        return

    # Se obtiene la tarea con el ID ingresado
    task_tuple = manager.get_task_by_id(task_id)
    if task_tuple[1] is False:
        console.print("[bold red]Error: La tarea no existe.[/bold red]")
        return

    task = task_tuple[0]
    show_one_task(console, task)
    if confirm("¿Está seguro de que quiere eliminar la tarea?"):
        try:
            manager.delete_task_by_id(task_id)
            console.print("[bold green]Tarea eliminada.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")


def show_tasks(manager: TaskManager, console: Console):
    tasks = manager.get_tasks()
    if len(tasks) == 0:
        console.print("[bold]No hay tareas.[/bold]")
    else:
        show_tasks_table(console, tasks)


def reset_tasks(manager: TaskManager, console: Console):
    if confirm("¿Está seguro de que quiere resetear las tareas?"):
        try:
            manager.reset_tasks()
            console.print("[bold green]Tareas reseteadas.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")


def generate_report(report_gen: ReportGenerator, console: Console):
    # Pedir fecha de inicio y fin
    start_date = get_date(
        console, "Ingrese la fecha de inicio del reporte (YYYY-MM-DD): ", "%Y-%m-%d"
    )
    end_date = get_date(
        console, "Ingrese la fecha de fin del reporte (YYYY-MM-DD): ", "%Y-%m-%d"
    )

    # Pedir salario por hora
    salary = prompt("Ingrese su salario por hora: ")
    salary = check_float(console, salary)
    if salary == -1:
        console.print(
            "[bold red]Error: El salario debe ser un número valido.[/bold red]"
        )
        return

    try:
        report_gen.generate_report(start_date, end_date, salary)
        console.print("[bold green]Reporte generado.[/bold green]")
    except ValueError:
        console.print(
            "[bold red]Fecha inválida. Asegúrese de ingresar las fechas en el formato correcto (YYYY-MM-DD).[/bold red]"
        )


def start_new_task(manager: TaskManager, console: Console):
    task = manager.start_task()
    start_time = arrow.now()
    console.print(
        f"Tarea iniciada a las [bold green]{start_time.format('YYYY-MM-DD HH:mm:ss')}[/bold green]."
    )

    console.print("Presione [bold red]Ctrl+C[/bold red] para finalizar la tarea...")
    timer(console, start_time)

    desc = prompt("Descripción de la tarea: ")
    task.description = desc
    end_time = arrow.now()

    show_one_task(console, task)
    if not confirm("¿Desea guardar la tarea?"):
        return

    manager.end_task(task)
    duration = end_time - start_time
    console.print(
        f"\nTarea finalizada a las [bold green]{end_time.format('YYYY-MM-DD HH:mm:ss')}[/bold green]. Duración total: [bold]{str(duration)}[/bold]"
    )


if __name__ == "__main__":
    main()
