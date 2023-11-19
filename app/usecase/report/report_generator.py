import pandas as pd
from app.routers.database import Database
from datetime import datetime, time

class ReportGenerator:
    def __init__(self):
        self.db = Database()
        self.df = None  # Agregar una propiedad para el DataFrame

    def generate_report(self, start_date, end_date, filename='report.xlsx'):
        start_datetime = datetime.combine(start_date, time())
        end_datetime = datetime.combine(end_date, time())

        tasks = self.db.get_tasks()
        data = []
        for task in tasks:
            if start_datetime <= task.start_time <= end_datetime:
                duration = (task.end_time - task.start_time).total_seconds() / 3600  # Convertir a horas
                data.append((task.id, task.start_time.strftime("%Y-%m-%d %H:%M:%S"), task.end_time.strftime("%Y-%m-%d %H:%M:%S"), task.description, duration))
        
        self.df = pd.DataFrame(data, columns=['ID', 'Start Time', 'End Time', 'Description', 'Duration'])
        self.df.to_excel(filename, index=False)
