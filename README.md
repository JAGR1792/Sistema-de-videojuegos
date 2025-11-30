# Plataforma de Videojuegos

Este proyecto implementa una plataforma de videojuegos conceptual utilizando Python y Flask, aplicando principios de Programacion Orientada a Objetos (POO) y Patrones de Diseno. Incluye una interfaz web para interactuar con el sistema.

## Estructura del Proyecto

- `app.py`: Aplicacion Flask principal y rutas web.
- `src/`: Codigo fuente del dominio (Modelos, Patrones, Servicios).
- `templates/`: Plantillas HTML (Jinja2) para la interfaz de usuario.
- `static/`: Archivos estaticos (CSS).
- `Procfile`: Archivo de configuracion para despliegue en Render/Heroku.
- `requirements.txt`: Dependencias del proyecto.

## Arquitectura y Patrones

### 1. Abstraccion e Interfaces
Se utiliza la clase abstracta `Videojuego` como base. Interfaces definidas: `Multijugador`, `ConMicrotransacciones`, `Actualizable`, `Calificable`.

### 2. Patron Factory
`JuegoFactory` centraliza la creacion de juegos (`src/patterns/factory.py`).

### 3. Patron Strategy
Estrategias de Matchmaking (`Aleatorio`, `PorRango`) intercambiables en tiempo de ejecucion (`src/patterns/strategy.py`).

### 4. Patron Observer
Sistema de notificaciones para logros y actualizaciones (`src/patterns/observer.py`).

## Instalacion y Ejecucion Local

1.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ejecutar la aplicacion:
    ```bash
    python app.py
    ```
3.  Abrir en el navegador: `http://127.0.0.1:5000`

## Despliegue en Render

Este proyecto esta configurado para ser desplegado facilmente en Render.com.

1.  Sube este codigo a un repositorio de GitHub.
2.  Crea una cuenta en [Render](https://render.com).
3.  Selecciona "New Web Service".
4.  Conecta tu repositorio.
5.  Render detectara automaticamente la configuracion, pero asegurate de:
    -   **Build Command:** `pip install -r requirements.txt`
    -   **Start Command:** `gunicorn app:app`
6.  Haz clic en "Create Web Service".

El archivo `Procfile` incluido asegura que Render sepa exactamente como iniciar la aplicacion usando Gunicorn para un rendimiento optimo en produccion.
