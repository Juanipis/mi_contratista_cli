import pandas as pd
from app.routers.database import Database
from datetime import datetime, time


class ReportGenerator:
    def __init__(self):
        self.db = Database()
        self.df = None

    def generate_report(
        self,
        start_date: datetime,
        end_date: datetime,
        salary: float,
        filename="report.xlsx",
    ):
        start_datetime = datetime.combine(start_date, time())
        end_datetime = datetime.combine(end_date, time())

        tasks = self.db.get_tasks()
        data = []
        for task in tasks:
            if start_datetime <= task.start_time <= end_datetime:
                duration = (task.end_time - task.start_time).total_seconds() / 3600
                data.append(
                    (
                        task.id,
                        task.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        task.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        task.description,
                        duration,
                    )
                )

        self.df = pd.DataFrame(
            data, columns=["ID", "Start Time", "End Time", "Description", "Duration"]
        )

        # Calcular y añadir la fila de total de horas
        total_hours = self.df["Duration"].sum()
        total_row = pd.DataFrame(
            [["Total", "", "", "", total_hours]], columns=self.df.columns
        )
        self.df = pd.concat([self.df, total_row], ignore_index=True)

        # Calcular y añadir la fila de pago total
        total_payment = salary * total_hours
        payment_row = pd.DataFrame(
            [["Pago Total", "", "", "", total_payment]], columns=self.df.columns
        )
        self.df = pd.concat([self.df, payment_row], ignore_index=True)

        self.df.to_excel(filename, index=False)
