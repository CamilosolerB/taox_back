# Documentación del módulo de autenticación

## Estructura implementada

### 1. Archivos de Seguridad (`app/core/security.py`)
- `hash_password()` - Hash de contraseñas con bcrypt
- `verify_password()` - Verificación de contraseñas
- `create_access_token()` - Generación de tokens JWT
- `decode_token()` - Decodificación y validación de JWT
- `get_user_from_token()` - Extracción de ID de usuario desde token

### 2. Middlewares (`app/core/middleware/auth_middleware.py`)
- `get_current_user()` - Valida JWT y retorna datos del usuario autenticado
- `require_admin()` - Middleware para proteger endpoints que requieren rol de administrador
- `require_observer()` - Middleware para proteger endpoints que requieren rol de observador o administrador

### 3. DTOs de Autenticación
- `RegisterDTO` - Para registro de nuevos usuarios
- `LoginDTO` - Para login de usuarios
- `TokenDTO` - Respuesta con token JWT
- `TokenPayloadDTO` - Estructura del payload del JWT

### 4. Use Cases
- `RegisterUserUseCase` - Registra un usuario con contraseña hasheada
- `LoginUserUseCase` - Autentica un usuario y retorna JWT

### 5. Endpoints de Autenticación (`/auth`)
- `POST /auth/register` - Registra un nuevo usuario
- `POST /auth/login` - Autentica y retorna token
- `GET /auth/me` - Obtiene info del usuario actual (requiere autenticación)

## Configuración del .env

Agrega estas variables a tu archivo `.env`:

```env
STAGE=development
DB_URL=postgresql://user:password@localhost/dbname
JWT_SECRET_KEY=tu_secreto_jwt_muy_seguro_aqui
ADMIN_ROLE_ID=uuid-del-rol-admin-aqui
OBSERVER_ROLE_ID=uuid-del-rol-observer-aqui
```

## Cómo usar

### 1. Registrar un usuario
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "securepassword123",
    "role_id": "uuid-del-rol-admin-aqui",
    "company_id": "uuid-de-la-company-aqui"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "uuid-usuario",
  "username": "john",
  "role_id": "uuid-rol"
}
```

### 3. Usar el token en requests

Todos los endpoints protegidos requieren el header de autorización:

```bash
curl -H "Authorization: Bearer {access_token}" \
  "http://localhost:8000/users/"
```

## Protección por Endpoints

### Endpoints públicos (sin protección)
- `GET /` - Root
- `POST /auth/register` - Registro
- `POST /auth/login` - Login

### Endpoints con autenticación requerida (cualquier usuario autenticado)
- `GET /auth/me` - Info del usuario actual
- `GET /users/` - Listar usuarios
- `GET /users/{user_id}` - Obtener usuario específico
- `GET /companies/` - Listar companies
- `GET /companies/{id}` - Obtener company específica
- `GET /products/` - Listar productos
- `GET /products/by-id/{id}` - Obtener producto por ID
- `GET /products/by-company/{company_id}` - Productos de una company

### Endpoints con rol de administrador requerido
- `POST /users/` - Crear usuario
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario
- `POST /companies/` - Crear company
- `PUT /companies/{id}` - Actualizar company
- `DELETE /companies/{id}` - Eliminar company
- `POST /products/` - Crear producto
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto

## Características de seguridad

✅ **Contraseñas hasheadas**: Uso de bcrypt con salt automático  
✅ **JWT con expiración**: Tokens expiran en 30 minutos  
✅ **Validación de roles**: Control de acceso por administrador/observador  
✅ **Middleware de autenticación**: En todos los endpoints protegidos  
✅ **Validación de email**: El DTO usa EmailStr de Pydantic  

## Próximos pasos opcional

1. Implementar refresh tokens para extender sesiones
2. Agregar rate limiting para endpoints de login/register
3. Implementar logout/token blacklist
4. Agregar two-factor authentication
5. Implementar rol-based access control (RBAC) más granular
