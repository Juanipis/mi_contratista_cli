
# Mi contratista cli

Este proyecto es una aplicación de gestión de tareas que permite a los usuarios iniciar tareas, generar informes, insertar tareas manualmente, mostrar tareas, resetear tareas y salir del programa. Utiliza Python 3.10 y `pipenv` para la gestión de entornos virtuales.

## Requisitos

- Python 3.10
- Pipenv

## Configuración del Proyecto

Primero, asegúrate de tener instalado Python 3.10 y Pipenv. Luego, clona este repositorio a tu máquina local.

## Instalación

Para configurar el entorno virtual y instalar las dependencias del proyecto, ejecuta:

```bash
pipenv install
```

## Ejecución

Para ejecutar la aplicación, primero activa el entorno virtual:

```bash
pipenv shell
```

Luego, inicia la aplicación con:

```bash
python ./app/main.py
```

## Uso

Una vez que la aplicación esté en ejecución, se presentarán varias opciones:

1. **Iniciar una Nueva Tarea**: Inicia el seguimiento de una nueva tarea.
2. **Generar un Reporte**: Genera un informe basado en un rango de fechas.
3. **Insertar Tarea Manualmente**: Permite la inserción manual de tareas con fechas y descripciones específicas.
4. **Mostrar las Tareas**: Muestra todas las tareas almacenadas.
5. **Resetear las Tareas**: Elimina todas las tareas almacenadas.
6. **Salir**: Sale de la aplicación.

Selecciona una opción usando su número correspondiente e ingresa la información requerida según las indicaciones.

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Por favor, asegúrate de seguir las mejores prácticas de programación y manten la coherencia con el estilo de código existente.
