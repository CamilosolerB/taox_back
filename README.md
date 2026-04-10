# taox_back

> [!TIP]
> **¿Eres nuevo en esto?** Si no eres desarrollador y quieres instalar este proyecto, sigue nuestra [Guía de Instalación Detallada](../GUIA_INSTALACION.md).

## Descripción General

`taox_back` es el componente de backend de una aplicación, desarrollado en Python utilizando el framework FastAPI. Este proyecto sigue una arquitectura modular y está diseñado para ser escalable y mantenible, proporcionando una API robusta para la gestión de datos y lógica de negocio.

## Características Principales

*   **API RESTful:** Implementación de endpoints RESTful para interactuar con la base de datos y la lógica de negocio.
*   **Autenticación y Autorización:** Gestión de usuarios y permisos.
*   **Base de Datos:** Integración con PostgreSQL utilizando SQLAlchemy para la persistencia de datos.
*   **Validación de Datos:** Uso de Pydantic para la validación de esquemas de datos de entrada y salida.
*   **Documentación Automática:** Generación automática de documentación de API (Swagger UI / ReDoc) gracias a FastAPI.

## Arquitectura Propuesta

El proyecto sigue una arquitectura limpia y modular, separando las responsabilidades en capas:

```bash
project/
│
├── app/
│   ├── api/                    # Interface layer
│   │   ├── routes/
│   │   │   └── users.py
│   │   └── dependencies/
│   │       └── db.py
│   │
│   ├── core/                   # Config global
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── domain/                 # Entidades y interfaces abstractas
│   │   ├── models/
│   │   │   └── user.py
│   │   └── repositories/
│   │       └── user_repository.py
│   │
│   ├── infrastructure/         # Implementaciones concretas
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── entities.py     # SQLAlchemy tables
│   │   └── repositories/
│   │       └── user_dao.py     # DAO
│   │
│   ├── services/               # Application / Use cases
│   │   └── user_service.py
│   │
│   ├── schemas/                # Pydantic request/response
│   │   └── user_schema.py
│   │
│   └── main.py                 # Punto de entrada FastAPI
│
├── tests/
│   └── ...
│
├── requirements.txt
└── README.md

```

## Tecnologías Utilizadas

*   **Python**
*   **FastAPI:** Framework web para construir APIs con Python.
*   **SQLAlchemy:** ORM (Object-Relational Mapper) para interactuar con la base de datos.
*   **Pydantic:** Biblioteca para la validación de datos y la gestión de configuraciones.
*   **PostgreSQL:** Base de datos relacional.
*   **Alembic:** Herramienta de migraciones de base de datos para SQLAlchemy.
*   **Uvicorn:** Servidor ASGI para ejecutar aplicaciones FastAPI.

## Instalación y Configuración

Para configurar y ejecutar el proyecto localmente, sigue los siguientes pasos:

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/CamilosolerB/taox_back.git
    cd taox_back
    ```

2.  **Crear y activar un entorno virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate   # En Windows
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**

    Crea un archivo `.env` en la raíz del proyecto con las siguientes variables (ejemplo):

    ```env
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    SECRET_KEY="tu_clave_secreta_aqui"
    ```

5.  **Ejecutar migraciones de base de datos:**

    ```bash
    alembic upgrade head
    ```

6.  **Iniciar el servidor:**

    ```bash
    uvicorn app.main:app --reload
    ```

    La API estará disponible en `http://127.0.0.1:8000`.
    La documentación interactiva (Swagger UI) estará en `http://127.0.0.1:8000/docs`.

## Uso de la API

(Aquí se pueden añadir ejemplos de endpoints y cómo interactuar con ellos, por ejemplo, para autenticación o CRUD de recursos específicos. Esto se puede detallar más una vez se conozcan los modelos específicos de la API.)

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un *issue* o *pull request* con tus sugerencias o mejoras.
