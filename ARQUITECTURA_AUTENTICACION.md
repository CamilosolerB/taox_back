# Estructura del Módulo de Autenticación

```bash
app/
├── core/
│   ├── security.py                    ← Funciones de hash y JWT
│   └── middleware/
│       ├── __init__.py
│       ├── auth_middleware.py         ← Middlewares por rol
│       └── USAGE_EXAMPLES.py          ← Ejemplos de uso
│
├── application/
│   ├── dto/
│   │   └── auth_dto/
│   │       ├── __init__.py
│   │       └── auth_dto.py            ← DTOs (Register, Login, Token)
│   │
│   └── use_cases/
│       └── auth_case/
│           ├── __init__.py
│           ├── register_user.py       ← Use case de registro (hashea pass)
│           └── login_user.py          ← Use case de login (genera JWT)
│
├── infrastructure/
│   ├── config/
│   │   └── auth_dependencies.py       ← Inyección de dependencias
│   │
│   └── adapters/
│       └── into/
│           └── http/
│               └── auth.py            ← Endpoints /auth/register, /auth/login
│
├── settings.py                        ← Configuración con JWT_SECRET_KEY
└── main.py                            ← Router de auth incluido
```

## Flujo de Autenticación

```bash
1. REGISTRO
   │
   ├─→ POST /auth/register
   │   ├─ ValidateEmail (no debe existir)
   │   ├─ hash_password(password) → bcrypt
   │   ├─ create_user() con password hasheada
   │   ├─ create_access_token()
   │   └─ Retorna Token
   │
2. LOGIN
   │
   ├─→ POST /auth/login
   │   ├─ get_user_by_email()
   │   ├─ verify_password(input, hash_db)
   │   ├─ create_access_token()
   │   └─ Retorna Token
   │
3. REQUEST PROTEGIDO
   │
   ├─→ GET /users/ (con Authorization header)
   │   ├─ Extraer token del header
   │   ├─ decode_token()
   │   ├─ Verificar expiración
   │   ├─ [Opcional] Verificar role_id
   │   └─ Permitir/Denegar acceso
```

## Características de Seguridad

```bash
┌─────────────────────────────────────────────────────────────┐
│ CONTRASEÑAS                                                 │
├─────────────────────────────────────────────────────────────┤
│ ✅ Hasheadas con bcrypt (10 rounds de salt)                │
│ ✅ Nunca se almacenan en texto plano                        │
│ ✅ Validadas con verify_password() en login                │
│ ✅ Cada hash es único aunque sea la misma contraseña        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TOKENS JWT                                                  │
├─────────────────────────────────────────────────────────────┤
│ ✅ Firmados con SECRET_KEY (HMAC-SHA256)                   │
│ ✅ Expiran en 30 minutos (configurable)                     │
│ ✅ Incluyen user_id, username, role_id, company_id         │
│ ✅ Validados en cada request protegido                      │
│ ✅ No se pueden modificar sin el SECRET_KEY                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CONTROL DE ACCESO POR ROLES                                │
├─────────────────────────────────────────────────────────────┤
│ ✅ require_admin() - Protege endpoints administrativos      │
│ ✅ require_observer() - Permite admin + observer            │
│ ✅ get_current_user() - Solo requiere autenticación         │
│ ✅ Validación antes de ejecutar la lógica de negocio        │
└─────────────────────────────────────────────────────────────┘
```

## Protección por Endpoints

| Endpoint | Método | Autenticación | Rol Requerido |
|----------|--------|---------------|---------------|
| /auth/register | POST | ❌ | N/A |
| /auth/login | POST | ❌ | N/A |
| /auth/me | GET | ✅ | Cualquier |
| /users/ | GET | ✅ | Cualquier |
| /users/ | POST | ✅ | Admin |
| /users/{id} | GET | ✅ | Cualquier |
| /users/{id} | PUT | ✅ | Admin |
| /users/{id} | DELETE | ✅ | Admin |
| /companies/ | GET | ✅ | Cualquier |
| /companies/ | POST | ✅ | Admin |
| /companies/{id} | GET | ✅ | Cualquier |
| /companies/{id} | PUT | ✅ | Admin |
| /companies/{id} | DELETE | ✅ | Admin |
| /products/ | GET | ✅ | Cualquier |
| /products/ | POST | ✅ | Admin |
| /products/by-id/{id} | GET | ✅ | Cualquier |
| /products/by-company/{id} | GET | ✅ | Cualquier |
| /products/{id} | PUT | ✅ | Admin |
| /products/{id} | DELETE | ✅ | Admin |
| /roles/ | GET | ✅ | Cualquier |
| /roles/ | POST | ✅ | Admin |

## Configuración Requerida (.env)

```bash
JWT_SECRET_KEY=tu_secreto_muy_seguro_aqui_cambiar_en_produccion
ADMIN_ROLE_ID=550e8400-e29b-41d4-a716-446655440000
OBSERVER_ROLE_ID=550e8400-e29b-41d4-a716-446655440001
```

## Ejemplos de Uso

### Registrarse

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "role_id": "550e8400-e29b-41d4-a716-446655440000",
    "company_id": "550e8400-e29b-41d4-a716-446655440002"
  }'
```

### Hacer login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Usar token en request protegido

```bash
curl -X GET http://localhost:8000/users/ \
  -H "Authorization: Bearer <token_recibido>"
```

### Obtener info del usuario actual

```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <token_recibido>"
```
