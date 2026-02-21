# Guía de Excepciones del Módulo de Autenticación

## Descripción General

Las excepciones personalizadas del módulo de autenticación están centralizadas en `app/core/exceptions.py`. Cada excepción tiene un código de error único y un mensaje default para facilitar el manejo de errores en los endpoints HTTP.

---

## Jerarquía de Excepciones

```
Exception
├── AuthenticationException (base)
    ├── InvalidCredentialsException
    ├── UserInactiveException
    ├── UserAlreadyExistsException
    ├── InvalidTokenException
    ├── TokenExpiredException
    ├── InsufficientPermissionsException
    ├── InvalidPasswordException
    ├── InvalidUsernameException
    └── InvalidEmailException
```

---

## Excepciones Disponibles

### 1. **InvalidCredentialsException**
- **Código de Error:** `AUTH_001`
- **Mensaje Default:** "Invalid email or password"
- **HTTP Status Code:** 401 Unauthorized
- **Casos de Uso:**
  - User no existe con ese email
  - Contraseña incorrecta
  - Login fallido

**Ejemplo:**
```python
from app.core.exceptions import InvalidCredentialsException

try:
    # Verificar contraseña
    if not verify_password(password, user.password):
        raise InvalidCredentialsException()
except InvalidCredentialsException as e:
    raise HTTPException(
        status_code=401,
        detail=e.default_message
    )
```

---

### 2. **UserInactiveException**
- **Código de Error:** `AUTH_002`
- **Mensaje Default:** "User account is inactive"
- **HTTP Status Code:** 403 Forbidden
- **Casos de Uso:**
  - Intento de login con cuenta inactiva
  - Validación middleware de usuario inactivo

**Ejemplo:**
```python
from app.core.exceptions import UserInactiveException

if not user.is_active:
    raise UserInactiveException()
```

---

### 3. **UserAlreadyExistsException**
- **Código de Error:** `AUTH_003`
- **Mensaje Default:** "User with this email already exists"
- **HTTP Status Code:** 409 Conflict
- **Casos de Uso:**
  - Intento de registro con email duplicado
  - Verificación de unicidad antes de crear

**Ejemplo:**
```python
from app.core.exceptions import UserAlreadyExistsException

if self.user_repository.get_user_by_email(email) is not None:
    raise UserAlreadyExistsException()
```

---

### 4. **InvalidTokenException**
- **Código de Error:** `AUTH_004`
- **Mensaje Default:** "Invalid or expired token"
- **HTTP Status Code:** 401 Unauthorized
- **Casos de Uso:**
  - Token malformado
  - Token no puede decodificarse
  - Campos requeridos faltantes en token

**Ejemplo:**
```python
from app.core.exceptions import InvalidTokenException

try:
    payload = decode_token(token)
    if "sub" not in payload or "email" not in payload:
        raise InvalidTokenException()
except:
    raise InvalidTokenException()
```

---

### 5. **TokenExpiredException**
- **Código de Error:** `AUTH_005`
- **Mensaje Default:** "Token has expired"
- **HTTP Status Code:** 401 Unauthorized
- **Casos de Uso:**
  - Token JWT expirado
  - Timeout de sesión

**Ejemplo:**
```python
from app.core.exceptions import TokenExpiredException
from jose.exceptions import ExpiredSignatureError

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
except ExpiredSignatureError:
    raise TokenExpiredException()
```

---

### 6. **InsufficientPermissionsException**
- **Código de Error:** `AUTH_006`
- **Mensaje Default:** "Insufficient permissions"
- **HTTP Status Code:** 403 Forbidden
- **Casos de Uso:**
  - Usuario no tiene el rol requerido
  - Intento de acceso a endpoint admin sin permisos

**Ejemplo:**
```python
from app.core.exceptions import InsufficientPermissionsException

ADMIN_ROLE_ID = "uuid-del-admin"

if str(user_id_from_token.role_id) != ADMIN_ROLE_ID:
    raise InsufficientPermissionsException()
```

---

### 7. **InvalidPasswordException**
- **Código de Error:** `AUTH_007`
- **Mensaje Default:** "Password does not meet security requirements"
- **HTTP Status Code:** 400 Bad Request
- **Casos de Uso:**
  - Contraseña menor a 8 caracteres
  - Falta letra mayúscula, minúscula, dígito o carácter especial
  - Validación durante registro

**Ejemplo:**
```python
from app.core.exceptions import InvalidPasswordException
from app.core.validators import PasswordValidator

valid, error = PasswordValidator.validate(password)
if not valid:
    raise InvalidPasswordException(error)
```

---

### 8. **InvalidUsernameException**
- **Código de Error:** `AUTH_008`
- **Mensaje Default:** "Username does not meet requirements"
- **HTTP Status Code:** 400 Bad Request
- **Casos de Uso:**
  - Username menor a 3 caracteres
  - Username mayor a 50 caracteres
  - Contiene caracteres inválidos
  - Comienza con número

**Ejemplo:**
```python
from app.core.exceptions import InvalidUsernameException
from app.core.validators import UsernameValidator

valid, error = UsernameValidator.validate(username)
if not valid:
    raise InvalidUsernameException(error)
```

---

### 9. **InvalidEmailException**
- **Código de Error:** `AUTH_009`
- **Mensaje Default:** "Invalid email format"
- **HTTP Status Code:** 400 Bad Request
- **Casos de Uso:**
  - Email sin formato válido
  - Email sin @ o punto
  - Validación de formato básico

**Ejemplo:**
```python
from app.core.exceptions import InvalidEmailException
from app.core.validators import EmailValidator

if not EmailValidator.is_valid(email):
    raise InvalidEmailException()
```

---

## Mapeo de Excepciones a HTTP Status Codes

| Excepción | Status Code | Descripción |
|-----------|-------------|-------------|
| `InvalidCredentialsException` | 401 | Usuario no existe o contraseña incorrecta |
| `UserInactiveException` | 403 | Usuario existe pero está inactivo |
| `UserAlreadyExistsException` | 409 | Email ya registrado |
| `InvalidTokenException` | 401 | Token inválido o malformado |
| `TokenExpiredException` | 401 | Token expirado |
| `InsufficientPermissionsException` | 403 | Usuario sin permisos requeridos |
| `InvalidPasswordException` | 400 | Contraseña no cumple requisitos |
| `InvalidUsernameException` | 400 | Username no cumple requisitos |
| `InvalidEmailException` | 400 | Email con formato inválido |

---

## Patrón de Manejo en Endpoints

```python
from fastapi import HTTPException, status
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordException,
    InvalidUsernameException,
    InvalidEmailException,
    InvalidCredentialsException,
    UserInactiveException
)

@router.post("/auth/register")
def register(register_dto: RegisterDTO):
    try:
        user = register_use_case.execute(
            username=register_dto.username,
            email=register_dto.email,
            password=register_dto.password,
            role_id=register_dto.role_id,
            company_id=register_dto.company_id
        )
        return {"message": "User created successfully"}
    
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.default_message
        )
    except (InvalidPasswordException, InvalidUsernameException, InvalidEmailException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred"
        )


@router.post("/auth/login")
def login(login_dto: LoginDTO):
    try:
        token_data = login_use_case.execute(
            email=login_dto.email,
            password=login_dto.password
        )
        return token_data
    
    except UserInactiveException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.default_message
        )
    except InvalidCredentialsException as e:
        # No revelar si el usuario existe por seguridad
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
```

---

## Patrón de Manejo en Use Cases

```python
from app.core.exceptions import (
    InvalidPasswordException,
    UserAlreadyExistsException
)
from app.core.validators import validate_auth_credentials

class RegisterUserUseCase:
    def execute(self, username: str, email: str, password: str, 
                role_id: str, company_id: str):
        try:
            # Validar todas las credenciales
            validate_auth_credentials(username, email, password)
        except (InvalidPasswordException, InvalidUsernameException, InvalidEmailException) as e:
            logger.warning(f"Validation failed: {str(e)}")
            raise
        
        # Verificar si el usuario ya existe
        if self.user_repository.get_user_by_email(email) is not None:
            logger.warning(f"User already exists: {email}")
            raise UserAlreadyExistsException()
        
        # ... resto de lógica
        return created_user
```

---

## Patrón de Validación

```python
from app.core.validators import validate_auth_credentials
from app.core.exceptions import (
    InvalidPasswordException,
    InvalidUsernameException,
    InvalidEmailException
)

try:
    validate_auth_credentials(username, email, password)
except InvalidPasswordException as e:
    # Manejo específico de contraseña
    logger.error(f"Password error: {str(e)}")
except InvalidUsernameException as e:
    # Manejo específico de username
    logger.error(f"Username error: {str(e)}")
except InvalidEmailException as e:
    # Manejo específico de email
    logger.error(f"Email error: {str(e)}")
```

---

## Logging Recomendado

```python
import logging

logger = logging.getLogger(__name__)

# En validaciones
logger.warning(f"Validation failed: {str(exception)}")

# En intentos de login
logger.warning(f"Login attempt with non-existent email: {email}")
logger.warning(f"Login attempt with inactive user: {email}")
logger.warning(f"Invalid password for user: {email}")

# En registros
logger.error(f"User already exists: {email}")
logger.info(f"User registered successfully: {email}")

# En permisos
logger.warning(f"Unauthorized access attempt by user: {user_id}")
```

---

## Resumen

- **Excepciones centralizadas** en `app/core/exceptions.py`
- **Código de error único** para cada tipo de excepción
- **Mensaje default** para facilitar respuestas HTTP
- **Jerarquía clara** que facilita el manejo general o específico
- **HTTP Status Codes** mapeados correctamente para cada caso
- **Logging integrado** para auditoría y debugging
- **Seguridad** mantenida sin revelar información sensible

