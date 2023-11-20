import sqlite3
from typing import Tuple
from app.models.task import Task


class Database:
    def __init__(self, db_path="tasks.db"):
        self.db_path = db_path
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al conectar con la base de datos: {e}")

    def create_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al crear la tabla: {e}")

    def add_task(self, task: Task):
        try:
            query = (
                "INSERT INTO tasks (start_time, end_time, description) VALUES (?, ?, ?)"
            )
            self.conn.execute(query, (task.start_time, task.end_time, task.description))
            self.conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al agregar tarea: {e}")

    def get_tasks(self) -> list[Task]:
        try:
            query = "SELECT * FROM tasks"
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return [
                Task(id=row[0], start_time=row[1], end_time=row[2], description=row[3])
                for row in rows
            ]
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al obtener tareas: {e}")

    def reset_tasks(self):
        try:
            query = "DELETE FROM tasks"
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al resetear tareas: {e}")

    def get_task_by_id(self, id: int) -> Tuple[Task, bool]:
        try:
            query = "SELECT * FROM tasks WHERE id = ?"
            cur = self.conn.cursor()
            cur.execute(query, (id,))
            row = cur.fetchone()
            if row:
                return Task(
                    id=row[0], start_time=row[1], end_time=row[2], description=row[3]
                ), True
            else:
                return Task(), False
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al obtener tarea: {e}")

    def delete_task_by_id(self, id: int):
        try:
            query = "DELETE FROM tasks WHERE id = ?"
            self.conn.execute(query, (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al eliminar tarea: {e}")
