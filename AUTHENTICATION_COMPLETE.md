# Módulo de Autenticación - Documentación Completa

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura](#arquitectura)
3. [Componentes](#componentes)
4. [Flujos de Autenticación](#flujos-de-autenticación)
5. [Endpoints](#endpoints)
6. [Middlewares](#middlewares)
7. [Validadores](#validadores)
8. [Excepciones](#excepciones)
9. [Configuración](#configuración)
10. [Testing](#testing)

---

## Descripción General

El módulo de autenticación implementa un sistema completo de autorización y autenticación basado en:

- **JWT (JSON Web Tokens)** para tokens stateless
- **Bcrypt** para hashing seguro de contraseñas
- **Role-Based Access Control (RBAC)** con roles Admin y Observer
- **Validación integral** de credenciales
- **Logging completo** para auditoría

---

## Arquitectura

La arquitectura sigue el patrón **hexagonal architecture**:

```
HTTP Layer (FastAPI)
        ↓
Endpoints (auth.py)
        ↓
Use Cases (register_user.py, login_user.py)
        ↓
Domain Entities (User Model)
        ↓
Infrastructure (Repositories)
        ↓
Database (PostgreSQL)
```

### Capas

1. **HTTP / Presentation Layer**
   - Endpoints REST en `app/infrastructure/adapters/into/http/auth.py`
   - DTOs para request/response validation

2. **Application Layer**
   - Use cases en `app/application/use_cases/auth_case/`
   - Business logic centralizada

3. **Domain Layer**
   - User model en `app/domain/entities/user_model.py`
   - Ports en `app/domain/ports/out/user_repository.py`

4. **Infrastructure Layer**
   - Repositories para acceso a BD
   - Adaptadores ORM
   - Configuración de dependencias

5. **Core Layer**
   - Security utilities (password hashing, JWT)
   - Validators (password, email, username)
   - Exception handling
   - Middleware para autorizacion

---

## Componentes

### 1. **Core Security Module** (`app/core/security.py`)

**Funciones principales:**

```python
def hash_password(password: str) -> str:
    """Hashea una contraseña con bcrypt (10 rounds)"""

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica una contraseña contra su hash"""

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Crea un JWT token con 30 minutos de expiración"""

def decode_token(token: str) -> dict | None:
    """Decodifica y valida un JWT token"""

def is_token_expired(token: str) -> bool:
    """Verifica si un token está expirado sin decodificar"""
```

**Características:**
- Bcrypt con 10 rounds + salt automático
- JWT con algoritmo HS256
- Manejo de ExpiredSignatureError
- Logging de operaciones

---

### 2. **Validators Module** (`app/core/validators.py`)

**Clases:**

```python
class PasswordValidator:
    """Valida requisitos de contraseña:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un dígito
    - Al menos un carácter especial (!@#$%^&*...)
    """

class EmailValidator:
    """Validación básica de email (Pydantic hace lo principal)"""

class UsernameValidator:
    """Valida requisitos de username:
    - Entre 3-50 caracteres
    - Solo alphanumeric + ._-
    - No puede comenzar con número
    """
```

**Función principal:**

```python
def validate_auth_credentials(username: str, email: str, password: str) -> None:
    """Valida todas las credenciales en una sola llamada"""
```

---

### 3. **Exceptions Module** (`app/core/exceptions.py`)

**Jerarquía:**
- `AuthenticationException` (base)
  - `InvalidCredentialsException` (AUTH_001, 401)
  - `UserInactiveException` (AUTH_002, 403)
  - `UserAlreadyExistsException` (AUTH_003, 409)
  - `InvalidTokenException` (AUTH_004, 401)
  - `TokenExpiredException` (AUTH_005, 401)
  - `InsufficientPermissionsException` (AUTH_006, 403)
  - `InvalidPasswordException` (AUTH_007, 400)
  - `InvalidUsernameException` (AUTH_008, 400)
  - `InvalidEmailException` (AUTH_009, 400)

---

### 4. **DTOs** (`app/application/dto/auth_dto/auth_dto.py`)

```python
class RegisterDTO:
    username: str          # 3-50 chars
    email: EmailStr        # Validado por Pydantic
    password: str          # Min 8, con requisitos de seguridad
    role_id: UUID          # UUID del rol
    company_id: UUID       # UUID de la company

class LoginDTO:
    email: EmailStr        # Email del usuario
    password: str          # Contraseña

class TokenDTO:
    access_token: str      # JWT token
    token_type: str        # "bearer"
    user_id: UUID          # ID del usuario
    username: str          # Nombre del usuario
    email: str             # Email del usuario
    role_id: UUID          # ID del rol
    is_active: bool        # Estado del usuario

class CurrentUserDTO:
    user_id: UUID
    username: str
    email: str
    role_id: UUID
    company_id: UUID
    is_active: bool

class ErrorResponseDTO:
    error_code: str        # Ej: "AUTH_001"
    detail: str            # Mensaje de error
```

---

### 5. **Use Cases**

#### RegisterUserUseCase (`app/application/use_cases/auth_case/register_user.py`)

```python
def execute(username, email, password, role_id, company_id) -> User:
    """
    1. Valida credenciales (username, email, password)
    2. Verifica que el email sea único
    3. Hashea la contraseña con bcrypt
    4. Crea el usuario con is_active=True
    5. Retorna el usuario creado
    """
```

**Excepciones:**
- `InvalidPasswordException`: Contraseña insegura
- `InvalidUsernameException`: Username inválido
- `InvalidEmailException`: Email inválido
- `UserAlreadyExistsException`: Email duplicado

---

#### LoginUserUseCase (`app/application/use_cases/auth_case/login_user.py`)

```python
def execute(email, password) -> dict:
    """
    1. Busca el usuario por email
    2. Verifica que exista (sino InvalidCredentialsException)
    3. Valida contraseña con bcrypt
    4. Verifica que esté activo
    5. Crea JWT token con datos del usuario
    6. Retorna token y datos de usuario
    """
```

**Excepciones:**
- `InvalidCredentialsException`: Email no existe o contraseña incorrecta
- `UserInactiveException`: Usuario inactivo

**Token Payload:**
```json
{
  "sub": "user-id",
  "username": "john_doe",
  "email": "john@example.com",
  "role_id": "admin-role-id",
  "company_id": "company-id",
  "is_active": true
}
```

---

### 6. **Endpoints** (`app/infrastructure/adapters/into/http/auth.py`)

#### POST /auth/register

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "role_id": "550e8400-e29b-41d4-a716-446655440000",
  "company_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "username": "john_doe",
  "email": "john@example.com",
  "role_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true
}
```

**Errores:**
- 400: Credenciales inválidas
- 409: Email ya existe

---

#### POST /auth/login

**Request:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "username": "john_doe",
  "email": "john@example.com",
  "role_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true
}
```

**Errores:**
- 401: Email o contraseña inválidos
- 403: Usuario inactivo

---

#### GET /auth/me

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "username": "john_doe",
  "email": "john@example.com",
  "role_id": "550e8400-e29b-41d4-a716-446655440000",
  "company_id": "550e8400-e29b-41d4-a716-446655440001",
  "is_active": true
}
```

**Errores:**
- 401: Token inválido o expirado
- 403: Usuario inactivo

---

#### POST /auth/validate-token

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "valid": true,
  "expired": false,
  "user_id": "550e8400-e29b-41d4-a716-446655440002"
}
```

---

## Middlewares

### Auth Middleware (`app/core/middleware/auth_middleware.py`)

#### `get_current_user()` - Dependency

```python
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    """
    Extrae y valida el usuario del JWT token
    
    1. Decodifica el token
    2. Verifica que tenga todos los campos requeridos
    3. Verifica que el usuario esté activo
    4. Retorna el payload del token
    """
```

**Validaciones:**
- Token válido (no corrupto)
- Token no expirado
- Contiene `sub`, `email`, `username`, `role_id`, `company_id`, `is_active`
- Usuario status = `is_active: true`

---

#### `require_admin()` - Dependency

```python
async def require_admin(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    """Valida que el usuario sea Admin"""
```

**Configuración:**
```python
ADMIN_ROLE_ID = "admin-uuid-from-env"
```

---

#### `require_observer()` - Dependency

```python
async def require_observer(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    """Valida que el usuario sea Observer o Admin"""
```

---

#### Helper Functions

```python
def get_user_id_from_token(current_user: dict) -> str:
    """Extrae user_id del payload"""

def get_company_id_from_token(current_user: dict) -> str:
    """Extrae company_id del payload"""
```

---

## Flujos de Autenticación

### Flujo de Registro

```
1. Cliente POST /auth/register
   ├─ Envía: username, email, password, role_id, company_id
   
2. Endpoint register()
   ├─ Valida DTO con Pydantic
   
3. RegisterUserUseCase.execute()
   ├─ Llama validate_auth_credentials()
   │  ├─ PasswordValidator.validate()
   │  ├─ UsernameValidator.validate()
   │  └─ EmailValidator.is_valid()
   ├─ Verifica email único en BD
   ├─ Hashea contraseña (bcrypt)
   ├─ Crea usuario en BD
   └─ Retorna User

4. Automáticamente Login
   ├─ Llama LoginUserUseCase.execute()
   ├─ Crea JWT token
   └─ Retorna TokenDTO

5. Respuesta 201 Created
   └─ Cliente recibe access_token
```

---

### Flujo de Login

```
1. Cliente POST /auth/login
   ├─ Envía: email, password
   
2. Endpoint login()
   ├─ Valida DTO con Pydantic
   
3. LoginUserUseCase.execute()
   ├─ Busca usuario por email
   ├─ Si no existe: InvalidCredentialsException → 401
   ├─ Verifica contraseña (bcrypt)
   ├─ Si incorrecta: InvalidCredentialsException → 401
   ├─ Verifica is_active
   ├─ Si inactivo: UserInactiveException → 403
   ├─ Crea JWT token
   └─ Retorna token + user data

4. Respuesta 200 OK
   └─ Cliente recibe access_token
```

---

### Flujo de Acceso a Recurso Protegido

```
1. Cliente GET /api/users/{user_id}
   ├─ Header: Authorization: Bearer <token>
   
2. FastAPI oauth2_scheme
   ├─ Extrae token del header
   └─ Pasa a dependency
   
3. Endpoint con get_current_user dependency
   ├─ Llama get_current_user()
   
4. get_current_user()
   ├─ Decodifica token
   ├─ Si inválido/expirado: InvalidTokenException → 401
   ├─ Valida campos requeridos
   ├─ Verifica is_active
   ├─ Si inactivo: UserInactiveException → 403
   └─ Retorna current_user dict
   
5. Handler tiene acceso a current_user
   └─ Puede usar get_user_id_from_token() etc
   
6. Respuesta
   └─ 200 OK con datos
```

---

### Flujo de Validación de Permisos (Role-Based)

```
1. Cliente GET /api/admin/users
   ├─ Header: Authorization: Bearer <token>
   
2. Endpoint con require_admin dependency
   ├─ Llama require_admin()
   
3. require_admin()
   ├─ Primero llama get_current_user()
   │  └─ Valida token y user
   ├─ Obtiene role_id del payload
   ├─ Compara con ADMIN_ROLE_ID
   ├─ Si no coincide: InsufficientPermissionsException → 403
   └─ Retorna current_user
   
4. Handler tiene acceso a current_user
   ├─ Garantizado que es admin
   └─ Puede ejecutar lógica admin
   
5. Respuesta
   └─ 200 OK con datos
```

---

## Configuración

### Variables de Entorno (`.env`)

```env
# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Role Configuration
ADMIN_ROLE_ID=550e8400-e29b-41d4-a716-446655440100
OBSERVER_ROLE_ID=550e8400-e29b-41d4-a716-446655440101

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Imports Recomendados

```python
# En endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.middleware.auth_middleware import (
    get_current_user, 
    require_admin, 
    require_observer,
    get_user_id_from_token,
    get_company_id_from_token
)
from app.core.exceptions import *

# En use cases
from app.core.validators import validate_auth_credentials
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import *

# En validadores
from app.core.validators import (
    PasswordValidator,
    EmailValidator,
    UsernameValidator,
    validate_auth_credentials
)
```

---

## Testing

### Test de Registro

```python
def test_register_success(client):
    """Test registro exitoso"""
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "SecurePass123!",
        "role_id": "role-uuid",
        "company_id": "company-uuid"
    })
    assert response.status_code == 201
    assert response.json()["access_token"]

def test_register_duplicate_email(client):
    """Test email duplicado"""
    # Primero registro exitoso
    client.post("/auth/register", json={...})
    
    # Segundo registro con mismo email
    response = client.post("/auth/register", json={...})
    assert response.status_code == 409

def test_register_weak_password(client):
    """Test contraseña débil"""
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "weak",  # No cumple requisitos
        "role_id": "role-uuid",
        "company_id": "company-uuid"
    })
    assert response.status_code == 400
```

### Test de Login

```python
def test_login_success(client):
    """Test login exitoso"""
    response = client.post("/auth/login", json={
        "email": "john@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    assert response.json()["access_token"]

def test_login_invalid_email(client):
    """Test email no existe"""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 401

def test_login_wrong_password(client):
    """Test contraseña incorrecta"""
    response = client.post("/auth/login", json={
        "email": "john@example.com",
        "password": "WrongPassword"
    })
    assert response.status_code == 401

def test_login_inactive_user(client):
    """Test usuario inactivo"""
    # Crear y desactivar usuario
    user.is_active = False
    user.save()
    
    response = client.post("/auth/login", json={
        "email": "john@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 403
```

### Test de Autorización

```python
def test_protected_route_with_token(client):
    """Test acceso a ruta protegida con token"""
    # Login primero
    login_response = client.post("/auth/login", json={...})
    token = login_response.json()["access_token"]
    
    # Acceder a ruta protegida
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_protected_route_no_token(client):
    """Test acceso sin token"""
    response = client.get("/api/users/me")
    assert response.status_code == 401

def test_admin_route_without_admin_role(client):
    """Test acceso admin sin rol admin"""
    # Login con usuario observer
    login_response = client.post("/auth/login", json={
        "email": "observer@example.com",
        "password": "SecurePass123!"
    })
    token = login_response.json()["access_token"]
    
    # Intentar acceder a ruta admin
    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
```

---

## Resumen de Seguridad

✅ **Contraseñas:**
- Hasheadas con bcrypt (10 rounds)
- Nunca se almacenan en texto plano
- Validadas contra requisitos de complejidad

✅ **Tokens:**
- JWT con HS256 (HMAC)
- Expiran en 30 minutos
- Contienen datos del usuario para autorización
- Validados en cada request

✅ **Autorización:**
- Role-based access control
- Validación de permisos en middlewares
- Protección de endpoints sensibles

✅ **Validación:**
- Input validation en todos los endpoints
- DTOs con Pydantic
- Custom validators para reglas de negocio

✅ **Logging:**
- Todos los intentos de autenticación
- Fallos de validación
- Accesos a recursos protegidos

✅ **Mensajes de Error:**
- No revelan si usuario existe (prevenir enumeration)
- Específicos pero seguros
- Codes de error para debugging

