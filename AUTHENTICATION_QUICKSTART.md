# Autenticación - Quick Start Guide

## Configuración Rápida

### 1. Variables de Entorno

```bash
# .env
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ADMIN_ROLE_ID=550e8400-e29b-41d4-a716-446655440100
OBSERVER_ROLE_ID=550e8400-e29b-41d4-a716-446655440101
```

### 2. Crear Roles en Base de Datos

```sql
INSERT INTO roles (id, name, description, is_active)
VALUES 
  ('550e8400-e29b-41d4-a716-446655440100', 'Admin', 'Administrator', true),
  ('550e8400-e29b-41d4-a716-446655440101', 'Observer', 'Read-only observer', true);
```

### 3. Crear Company

```sql
INSERT INTO companies (id, name, rfc, address, phone, is_active)
VALUES 
  ('550e8400-e29b-41d4-a716-446655440001', 'Test Company', 'RFC123', 'Address', '1234567890', true);
```

---

## Uso de Endpoints

### Registro

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "role_id": "550e8400-e29b-41d4-a716-446655440100",
    "company_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "username": "john_doe",
  "email": "john@example.com",
  "role_id": "550e8400-e29b-41d4-a716-446655440100",
  "is_active": true
}
```

---

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

---

### Obtener Usuario Actual

```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

### Validar Token

```bash
curl -X POST http://localhost:8000/auth/validate-token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "<access_token>"
  }'
```

---

## Uso en Endpoints

### Endpoint Público (Sin Autenticación)

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/public")
def public_route():
    return {"message": "This is public"}
```

---

### Endpoint Autenticado (Requiere Token)

```python
from fastapi import APIRouter, Depends
from typing import Annotated
from app.core.middleware.auth_middleware import get_current_user

router = APIRouter()

@router.get("/users/me")
def get_current_user_info(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return {
        "user_id": current_user.get("sub"),
        "username": current_user.get("username"),
        "email": current_user.get("email")
    }
```

---

### Endpoint Solo para Admin

```python
from fastapi import APIRouter, Depends
from typing import Annotated
from app.core.middleware.auth_middleware import require_admin

router = APIRouter()

@router.get("/admin/users")
def get_all_users(
    current_user: Annotated[dict, Depends(require_admin)]
):
    # Solo admin puede acceder
    return {"users": [...]}
```

---

### Endpoint para Admin u Observer

```python
from fastapi import APIRouter, Depends
from typing import Annotated
from app.core.middleware.auth_middleware import require_observer

router = APIRouter()

@router.get("/reports")
def get_reports(
    current_user: Annotated[dict, Depends(require_observer)]
):
    # Admin y Observer pueden acceder
    return {"reports": [...]}
```

---

### Acceder a Datos del Usuario en Handler

```python
from app.core.middleware.auth_middleware import (
    get_current_user,
    get_user_id_from_token,
    get_company_id_from_token
)

@router.get("/my-data")
def my_data(current_user: Annotated[dict, Depends(get_current_user)]):
    # Opción 1: Acceder directamente
    user_id = current_user.get("sub")
    email = current_user.get("email")
    role_id = current_user.get("role_id")
    
    # Opción 2: Usar helpers
    user_id = get_user_id_from_token(current_user)
    company_id = get_company_id_from_token(current_user)
    
    return {"user_id": user_id, "email": email}
```

---

## Validación de Inputs

### Validar Contraseña

```python
from app.core.validators import PasswordValidator

# En uso case o handler
valid, error = PasswordValidator.validate(password)
if not valid:
    raise InvalidPasswordException(error)
```

**Requisitos:**
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 minúscula
- Al menos 1 dígito
- Al menos 1 carácter especial (!@#$%^&*()_+-=[]{}|;:,.<>?)

---

### Validar Username

```python
from app.core.validators import UsernameValidator

valid, error = UsernameValidator.validate(username)
if not valid:
    raise InvalidUsernameException(error)
```

**Requisitos:**
- Entre 3-50 caracteres
- Solo alphanumeric + . _ -
- No puede empezar con número

---

### Validar Email

```python
from app.core.validators import EmailValidator

if not EmailValidator.is_valid(email):
    raise InvalidEmailException()
```

---

## Manejo de Excepciones

### En Endpoints

```python
from fastapi import HTTPException, status
from app.core.exceptions import (
    InvalidCredentialsException,
    UserInactiveException,
    UserAlreadyExistsException,
    InsufficientPermissionsException
)

@router.post("/auth/login")
def login(login_dto: LoginDTO, login_use_case: LoginUserUseCase):
    try:
        return login_use_case.execute(
            email=login_dto.email,
            password=login_dto.password
        )
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    except UserInactiveException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
```

---

### En Use Cases

```python
from app.core.exceptions import UserAlreadyExistsException

def execute(self, email: str, ...):
    if self.user_repository.get_user_by_email(email) is not None:
        raise UserAlreadyExistsException()
```

---

## Logging

### Logging de Autenticación

```python
import logging

logger = logging.getLogger(__name__)

# En login
logger.info(f"Login exitoso: {email}")
logger.warning(f"Intento de login fallido: {email}")

# En registro
logger.info(f"Usuario registrado: {email}")
logger.warning(f"Email duplicado: {email}")

# En validación
logger.warning(f"Validación fallida: {error_message}")
```

---

## Estructura de Archivos

```
app/
├── core/
│   ├── security.py                    # JWT + Bcrypt
│   ├── validators.py                  # Password, Email, Username validators
│   ├── exceptions.py                  # Custom exceptions
│   └── middleware/
│       └── auth_middleware.py         # JWT middleware
├── application/
│   ├── dto/
│   │   └── auth_dto/
│   │       └── auth_dto.py           # DTOs (Register, Login, Token)
│   └── use_cases/
│       └── auth_case/
│           ├── register_user.py       # Registration logic
│           └── login_user.py          # Login logic
└── infrastructure/
    ├── adapters/
    │   └── into/
    │       └── http/
    │           └── auth.py            # HTTP endpoints
    └── config/
        └── auth_dependencies.py       # Dependency injection
```

---

## Contraseñas Válidas

✅ Ejemplos válidos:
- `SecurePass123!`
- `MyP@ssw0rd`
- `Test@1234`
- `Admin#2024Pass`

❌ Ejemplos inválidos:
- `short` (muy corta)
- `nouppercase123!` (sin mayúscula)
- `NOLOWERCASE123!` (sin minúscula)
- `NoDigits!` (sin número)
- `NoSpecial123` (sin carácter especial)

---

## Usernames Válidos

✅ Ejemplos válidos:
- `john_doe`
- `user.name`
- `admin-user`
- `test123`

❌ Ejemplos inválidos:
- `ab` (muy corto)
- `123user` (empieza con número)
- `user@name` (carácter inválido)
- `a` (muy corto)

---

## Emails

Cualquier email válido en formato estándar:
- `john@example.com`
- `user.name+tag@domain.co.uk`

❌ Inválidos:
- `invalid` (sin @)
- `user@` (sin dominio)

---

## Errores Comunes

### 401 Unauthorized
- Email no existe
- Contraseña incorrecta
- Token inválido o expirado
- No se incluye Authorization header

**Solución:**
```bash
# Verificar que includes bearer token
curl -H "Authorization: Bearer <token>"
```

---

### 403 Forbidden
- Usuario inactivo
- Rol insuficiente (no es admin)
- Token válido pero permisos insuficientes

**Solución:**
- Verificar que usuario está activo en BD
- Verificar que ADMIN_ROLE_ID coincide con rol del usuario

---

### 409 Conflict
- Email ya existe en registro

**Solución:**
```bash
# Usar email diferente
curl ... -d '{"email": "newemail@example.com", ...}'
```

---

### 400 Bad Request
- Contraseña débil
- Username inválido
- Email inválido
- DTO validation error

**Solución:**
- Seguir requisitos de password/username
- Validar que datos cumplan con restricciones

---

## Testing Rápido

```python
# tests/test_auth.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!",
        "role_id": "role-uuid",
        "company_id": "company-uuid"
    })
    assert response.status_code == 201

def test_login():
    # Primero registrar
    client.post("/auth/register", json={...})
    
    # Luego login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123!"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Usar token
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

---

## Cheatsheet de Imports

```python
# Security
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    is_token_expired
)

# Validators
from app.core.validators import (
    PasswordValidator,
    EmailValidator,
    UsernameValidator,
    validate_auth_credentials
)

# Exceptions
from app.core.exceptions import (
    InvalidCredentialsException,
    UserInactiveException,
    UserAlreadyExistsException,
    InvalidTokenException,
    TokenExpiredException,
    InsufficientPermissionsException,
    InvalidPasswordException,
    InvalidUsernameException,
    InvalidEmailException
)

# Middleware
from app.core.middleware.auth_middleware import (
    get_current_user,
    require_admin,
    require_observer,
    get_user_id_from_token,
    get_company_id_from_token
)

# DTOs
from app.application.dto.auth_dto.auth_dto import (
    RegisterDTO,
    LoginDTO,
    TokenDTO,
    CurrentUserDTO,
    ErrorResponseDTO
)

# Use Cases
from app.application.use_cases.auth_case.register_user import RegisterUserUseCase
from app.application.use_cases.auth_case.login_user import LoginUserUseCase
```

---

## Notes

- Tokens válidos por 30 minutos (configurable en `.env`)
- Bcrypt con 10 rounds (seguro pero no lento)
- Todas las operaciones de auth están logueadas
- Middleware de auth en todos los endpoints protegidos
- Role-based access control con ADMIN_ROLE_ID y OBSERVER_ROLE_ID
- Validación integral de inputs

