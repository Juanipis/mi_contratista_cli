import sqlite3
from app.models.task import Task

class Database:
    def __init__(self, db_path='tasks.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
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

    def add_task(self, task: Task):
        query = "INSERT INTO tasks (start_time, end_time, description) VALUES (?, ?, ?)"
        self.conn.execute(query, (task.start_time, task.end_time, task.description))
        self.conn.commit()

    def get_tasks(self) -> list[Task]:
        query = "SELECT * FROM tasks"
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return [Task(id=row[0], start_time=row[1], end_time=row[2], description=row[3]) for row in rows]
    
    def reset_tasks(self):
        query = "DELETE FROM tasks"
        self.conn.execute(query)
        self.conn.commit()
