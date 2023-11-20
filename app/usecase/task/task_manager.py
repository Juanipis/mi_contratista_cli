from typing import Tuple
from app.models.task import Task
from app.routers.database import Database
from datetime import datetime, timedelta


class TaskManager:
    def __init__(self):
        self.db = Database()

    def round_start_time(self, time: datetime) -> datetime:
        if time.minute < 30:
            return time.replace(minute=0, second=0, microsecond=0)
        else:
            return time.replace(minute=30, second=0, microsecond=0)

    def round_end_time(self, time: datetime) -> datetime:
        if time.minute < 30:
            return time.replace(minute=30, second=0, microsecond=0)
        else:
            return (time + timedelta(hours=1)).replace(
                minute=0, second=0, microsecond=0
            )

    def start_task(self) -> Task:
        now = datetime.now()
        start_time = self.round_start_time(now)
        return Task(id=0, start_time=start_time, end_time=start_time)

    def end_task(self, task: Task):
        now = datetime.now()
        end_time = self.round_end_time(now)
        task.end_time = end_time
        self.db.add_task(task)

    def get_tasks(self) -> list[Task]:
        return self.db.get_tasks()

    def reset_tasks(self):
        self.db.reset_tasks()

    def add_task_manually(
        self, start_time: datetime, end_time: datetime, description: str
    ) -> bool:
        try:
            # Validar que start_time sea menor que end_time
            if start_time >= end_time:
                return False

            # Crear la tarea
            task = Task(
                id=0, start_time=start_time, end_time=end_time, description=description
            )

            # Agregar la tarea a la base de datos
            self.db.add_task(task)

            return True
        except Exception:
            return False

    def delete_task_by_id(self, id: int):
        self.db.delete_task_by_id(id)

    def get_task_by_id(self, id: int) -> Tuple[Task, bool]:
        return self.db.get_task_by_id(id)
