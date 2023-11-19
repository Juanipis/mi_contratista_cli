import unittest
from unittest.mock import MagicMock
from datetime import datetime
from app.models.task import Task
from app.routers.database import Database
from app.usecase.report.report_generator import ReportGenerator

class ReportGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()  # Crear un mock para Database
        self.report_generator = ReportGenerator()
        self.report_generator.db = self.db  # Reemplazar db en ReportGenerator con el mock

    def test_generate_report(self):
        # Crear datos mock para las tareas
        tasks = [
            Task(id=1, start_time=datetime(2023, 11, 18, 10, 0, 0), end_time=datetime(2023, 11, 18, 11, 0, 0), description="Tarea 1 hora"),
            Task(id=2, start_time=datetime(2023, 11, 18, 12, 0, 0), end_time=datetime(2023, 11, 18, 14, 0, 0), description="Tarea 2 horas"),
            Task(id=3, start_time=datetime(2023, 11, 18, 15, 0, 0), end_time=datetime(2023, 11, 18, 18, 0, 0), description="Tarea 3 horas"),
            Task(id=4, start_time=datetime(2023, 11, 18, 19, 0, 0), end_time=datetime(2023, 11, 18, 19, 30, 0), description="Tarea 0.5 horas"),
        ]
        self.db.get_tasks.return_value = tasks

        # Definir las fechas de inicio y fin para el informe
        start_date = datetime(2023, 11, 18)
        end_date = datetime(2023, 11, 19)

        # Generar el informe
        self.report_generator.generate_report(start_date, end_date, filename='test_report.xlsx')

        # Verificar que se llame al método get_tasks del objeto mock
        self.db.get_tasks.assert_called_once()
        
        # Verificar que el excel se haya generado correctamente verificando si las horas son correctas y el total de horas es correcto
        self.assertEqual(self.report_generator.df['Duration'].sum(), 6.5)

if __name__ == '__main__':
    unittest.main()