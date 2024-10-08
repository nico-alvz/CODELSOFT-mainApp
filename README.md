
# MainApp

Este proyecto es una API Flask que expone varios endpoints para la gestión de estudiantes, calificaciones y restricciones. La API incluye documentación Swagger para facilitar la visualización de los endpoints y sus esquemas.

## Requisitos

Antes de empezar, asegúrate de tener lo siguiente instalado:

- Python 3.11 o superior
- pip

## Instalación

Sigue los pasos a continuación para configurar el proyecto en tu máquina local:

1. Clona el repositorio con:
    ```bash
    git clone https://github.com/nico-alvz/CODELSOFT-mainApp.git
    ```
2. Crea un entorno virtual utilizando:
    ```bash
    python -m venv venv
    ```
   y actívalo.
3. Instala las dependencias con:
    ```bash
    pip install -r requirements.txt
    ```
4. Configura las variables de entorno en un archivo `.env`.
5. Ejecuta la aplicación localmente con:
    ```bash
    python run.py
    ```
   o utiliza Gunicorn para producción.

## Acceso a la Aplicación

Una vez que la aplicación esté corriendo, accede a la API en `http://localhost:5000` y la documentación Swagger en `http://localhost:5000/apidocs/`.

## Despliegue en Render

Este proyecto ya está desplegado en Render y puedes acceder a la aplicación en el siguiente enlace:

[Acceso al servicio desplegado](https://codelsoft-mainapp.onrender.com)
