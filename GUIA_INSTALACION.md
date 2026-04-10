# 🧠 Guía de Instalación: Backend (Servidor y API)

¡Hola! Esta guía es exclusiva para poner a funcionar el **Backend** (el cerebro del sistema). Si quieres ver la página web, también necesitarás instalar el repositorio de Frontend.

---

## 🛠️ Herramientas Necesarias

Antes de empezar, asegúrate de tener instalados estos dos programas:

### 1. Python
*   **Descarga**: [Haz clic aquí para descargar Python](https://www.python.org/downloads/windows/) (Recomendado: última versión estable).
*   **⚠️ IMPORTANTE**: Al instalar, marca la casilla **"Add Python to PATH"**.

### 2. PostgreSQL (Base de Datos)
*   **Descarga**: [Haz clic aquí para descargar PostgreSQL](https://www.postgresql.org/download/windows/).
*   **Instalación**: Recuerda la contraseña que elijas para el usuario `postgres`.

---

## 🚀 Pasos para la Instalación

1.  **Entra a la carpeta del proyecto**:
    Abre una terminal (CMD o PowerShell) en esta carpeta.
    
2.  **Crear el "Entorno Virtual"**:
    ```bash
    python -m venv venv
    ```
    
3.  **Activar el entorno**:
    ```bash
    venv\Scripts\activate
    ```
    *(Aparecerá `(venv)` al inicio de tu línea de comandos)*.

4.  **Instalar las librerías**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar la conexión a la base de datos**:
    - Busca el archivo `.env.example`.
    - Cámbiale el nombre a `.env`.
    - Edita la línea de `DB_URL` con tu contraseña de PostgreSQL:
      Ejemplo: `DB_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/tesis_db`

---

## 🏃 Cómo Iniciar el Servidor

Con el entorno activado (`venv`), ejecuta:
```bash
uvicorn app.main:app --reload
```
Si dice `Application startup complete`, el servidor está listo en `http://localhost:8000`.

---

## 🔗 Conexión con el Frontend
Recuerda que para usar el sistema completo necesitas la interfaz visual.
1. Instalar el repositorio de **Frontend**.
2. Asegurarte de que este servidor (Backend) esté corriendo antes de abrir la página web.
