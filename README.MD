
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
Primero es necesario un .env con las siguientes variables de entorno (se usa una base de datos postgresql):

```bash
db_host=
db_port=
db_user=
db_password=
db_name=
```
Para ejecutar la aplicación, primero activa el entorno virtual:

```bash
pipenv shell
```

Luego, inicia la aplicación con:

```bash
python ./app/main.py
```


## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Por favor, asegúrate de seguir las mejores prácticas de programación y manten la coherencia con el estilo de código existente.

