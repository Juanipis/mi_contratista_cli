from pydantic_settings import BaseSettings
import psycopg2
from psycopg2 import sql
from typing import Tuple
from app.models.task import Task


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str


class Database:
    def __init__(self):
        settings = Settings()
        self.conn = None
        self.connect(settings)
        self.create_table()

    def connect(self, settings: Settings):
        try:
            self.conn = psycopg2.connect(
                host=settings.db_host,
                port=settings.db_port,
                user=settings.db_user,
                password=settings.db_password,
                dbname=settings.db_name,
            )
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Error al conectar con la base de datos: {e}")

    def create_table(self):
        try:
            query = sql.SQL(
                """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """
            )
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Error al crear la tabla: {e}")

    def add_task(self, task: Task):
        try:
            query = sql.SQL(
                "INSERT INTO tasks (start_time, end_time, description) VALUES (%s, %s, %s)"
            )
            cur = self.conn.cursor()
            cur.execute(query, (task.start_time, task.end_time, task.description))
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Error al agregar tarea: {e}")

    def get_tasks(self) -> list[Task]:
        try:
            query = sql.SQL("SELECT * FROM tasks")
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return [
                Task(id=row[0], start_time=row[1], end_time=row[2], description=row[3])
                for row in rows
            ]
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Error al obtener tareas: {e}")

    def reset_tasks(self):
        try:
            query = sql.SQL("DELETE FROM tasks")
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Error al resetear tareas: {e}")

    def get_task_by_id(self, id: int) -> Tuple[Task, bool]:
        try:
            query = sql.SQL("SELECT * FROM tasks WHERE id = %s")
            cur = self.conn.cursor()
            cur.execute(query, (id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Task(
                    id=row[0], start_time=row[1], end_time=row[2], description=row[3]
                ), True
            else:
                return Task(), False
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Error al obtener tarea: {e}")

    def delete_task_by_id(self, id: int):
        try:
            query = sql.SQL("DELETE FROM tasks WHERE id = %s")
            cur = self.conn.cursor()
            cur.execute(query, (id,))
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Error al eliminar tarea: {e}")

    def close(self):
        self.conn.close()
