import time
from app.usecase.task.task_manager import TaskManager
from app.usecase.report.report_generator import ReportGenerator
from datetime import datetime
from rich.console import Console
from rich.table import Table
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm


def main():
    manager = TaskManager()
    report_gen = ReportGenerator()
    console = Console()

    while True:
        console.print("[bold magenta]Opciones disponibles:[/bold magenta]")
        options = [
            "Iniciar una nueva tarea",
            "Generar un reporte",
            "Insertar tarea manualmente",
            "Mostrar las tareas",
            "Resetear las tareas",
            "Salir",
        ]
        for i, option in enumerate(options, start=1):
            console.print(f"[bold cyan]{i}.[/bold cyan] {option}")

        option = prompt("Seleccione una opción: ")

        if option == "1":
            start_new_task(manager, console)

        elif option == "2":
            generate_report(report_gen, console)

        elif option == "3":
            # Se inserta manualmente una tarea, se pide la fecha de inicio, fecha de fin y descripción, las fechas deben tener sus respectivas horas
            start_time = prompt(
                "Ingrese la fecha de inicio de la tarea (YYYY-MM-DD HH:MM:SS): "
            )
            end_time = prompt(
                "Ingrese la fecha de fin de la tarea (YYYY-MM-DD HH:MM:SS): "
            )
            description = prompt("Ingrese la descripción de la tarea: ")

            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            if manager.add_task_manually(start_time, end_time, description):
                console.print("[bold green]Tarea agregada.[/bold green]")
            else:
                console.print(
                    "[bold red]Error al agregar tarea. Asegúrese de que la fecha de inicio sea menor que la fecha de fin.[/bold red]"
                )

        elif option == "4":
            show_tasks(manager, console)

        elif option == "5":
            reset_tasks(manager, console)

        elif option == "6":
            console.print("[bold yellow]Saliendo...[/bold yellow]")
            break
        else:
            console.print(
                "[bold red]Opción inválida. Por favor, seleccione una opción válida.[/bold red]"
            )


def show_tasks(manager, console):
    tasks = manager.get_tasks()
    if len(tasks) == 0:
        console.print("[bold]No hay tareas.[/bold]")
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Start Time")
        table.add_column("End Time")
        table.add_column("Description")
        for task in tasks:
            table.add_row(
                str(task.id),
                task.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                task.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                task.description,
            )
        console.print(table)


def reset_tasks(manager: TaskManager, console):
    if confirm("¿Está seguro de que quiere resetear las tareas?"):
        manager.reset_tasks()
        console.print("[bold green]Tareas reseteadas.[/bold green]")


def generate_report(report_gen, console):
    start_date = prompt("Ingrese la fecha de inicio del reporte (YYYY-MM-DD): ")
    end_date = prompt("Ingrese la fecha de fin del reporte (YYYY-MM-DD): ")
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        report_gen.generate_report(start_date, end_date)
        console.print("[bold green]Reporte generado.[/bold green]")
    except ValueError:
        console.print(
            "[bold red]Fecha inválida. Asegúrese de ingresar las fechas en el formato correcto (YYYY-MM-DD).[/bold red]"
        )


def start_new_task(manager, console):
    desc = prompt("Descripción de la tarea: ")
    task = manager.start_task(desc)
    start_time = datetime.now()
    console.print(
        f"Tarea iniciada a las [bold green]{start_time}[/bold green]. Descripción: '[bold]{task.description}'[/bold]"
    )

    console.print("Presione [bold red]Ctrl+C[/bold red] para finalizar la tarea...")
    try:
        with console.status("[bold green]Tarea en curso...[/bold green]") as status:
            while True:
                elapsed = datetime.now() - start_time
                status.update(f"Tiempo transcurrido: [bold]{elapsed}[/bold]")
                time.sleep(1)
    except KeyboardInterrupt:
        pass

    end_time = datetime.now()
    manager.end_task(task)
    console.print(
        f"\nTarea finalizada a las [bold green]{end_time}[/bold green]. Duración total: [bold]{end_time - start_time}[/bold]"
    )


if __name__ == "__main__":
    main()
