import unittest
from unittest.mock import Mock, patch
from app.main import start_new_task  # Asegúrate de importar correctamente tu función

class TestStartNewTask(unittest.TestCase):

    @patch('app.main.prompt', return_value="Descripción de prueba")
    @patch('app.main.Console')
    @patch('app.main.TaskManager')
    def test_start_new_task(self, mock_task_manager, mock_console, mock_prompt):
        # Configura los mocks
        mock_manager = mock_task_manager.return_value
        mock_manager.start_task.return_value = Mock(description="Tarea de prueba")

        # Llama a la función con los mocks
        start_new_task(mock_manager, mock_console)

        # Verifica que se haya iniciado y finalizado una tarea
        mock_manager.start_task.assert_called_once_with("Descripción de prueba")
        mock_manager.end_task.assert_called_once()

        # Verifica que prompt fue llamado
        mock_prompt.assert_called_once_with("Descripción de la tarea: ")

        # Puedes agregar más assertions aquí para verificar otros comportamientos esperados

if __name__ == '__main__':
    unittest.main()
