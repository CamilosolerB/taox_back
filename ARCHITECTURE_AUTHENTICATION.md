# Arquitectura del Sistema de Autenticación

## Vista General

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Client (Frontend)                    │
│           (Browser, Mobile App, API Client)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP Requests
                       │ (POST /auth/register, /auth/login, etc)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     FastAPI Application                       │
│                   (Presentation Layer)                        │
├──────────────────────────────────────────────────────────────┤
│  Routes:                                                       │
│  - POST /auth/register → register()                           │
│  - POST /auth/login → login()                                 │
│  - GET /auth/me → get_me()                                    │
│  - POST /auth/validate-token → validate_token()              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Depends()
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 Middleware & Dependencies                      │
│                  (Security Layer)                             │
├──────────────────────────────────────────────────────────────┤
│  - oauth2_scheme (OAuth2PasswordBearer)                       │
│  - get_current_user() → Validates JWT token                   │
│  - require_admin() → Checks role = ADMIN                      │
│  - require_observer() → Checks role = ADMIN or OBSERVER       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Calls
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      Use Cases                                │
│                (Application Layer)                            │
├──────────────────────────────────────────────────────────────┤
│  - RegisterUserUseCase                                        │
│    ├─ Validates credentials                                   │
│    ├─ Checks email uniqueness                                 │
│    └─ Creates user                                            │
│                                                               │
│  - LoginUserUseCase                                           │
│    ├─ Validates credentials                                   │
│    ├─ Checks user is active                                   │
│    └─ Creates JWT token                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Calls
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Domain & Core Logic                              │
│          (Domain & Core Layers)                              │
├──────────────────────────────────────────────────────────────┤
│  Security (app/core/security.py):                             │
│  - hash_password() → bcrypt hashing                           │
│  - verify_password() → bcrypt verification                    │
│  - create_access_token() → JWT creation                       │
│  - decode_token() → JWT validation                            │
│                                                               │
│  Validators (app/core/validators.py):                         │
│  - PasswordValidator                                          │
│  - EmailValidator                                             │
│  - UsernameValidator                                          │
│  - validate_auth_credentials()                                │
│                                                               │
│  Exceptions (app/core/exceptions.py):                         │
│  - InvalidCredentialsException                                │
│  - UserInactiveException                                      │
│  - UserAlreadyExistsException                                 │
│  - InvalidTokenException                                      │
│  - Etc.                                                       │
│                                                               │
│  DTOs (app/application/dto/auth_dto/):                        │
│  - RegisterDTO                                                │
│  - LoginDTO                                                   │
│  - TokenDTO                                                   │
│  - CurrentUserDTO                                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Uses
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Infrastructure Layer                         │
├──────────────────────────────────────────────────────────────┤
│  Repositories:                                                │
│  - UserRepository                                             │
│    ├─ get_user_by_email(email) → User | None                │
│    ├─ get_user_by_id(id) → User | None                      │
│    ├─ create_user(user) → User                               │
│    ├─ update_user(id, data) → User                           │
│    └─ delete_user(id) → None                                 │
│                                                               │
│  Dependencies (app/infrastructure/config/):                   │
│  - get_register_user_use_case()                               │
│  - get_login_user_use_case()                                  │
│  - get_user_repository()                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Queries/Updates
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Database Layer                              │
│                    (PostgreSQL)                               │
├──────────────────────────────────────────────────────────────┤
│  Users Table:                                                 │
│  - id_user (UUID primary key)                                 │
│  - username (varchar, unique)                                 │
│  - email (varchar, unique)                                    │
│  - password (varchar, hashed with bcrypt)                     │
│  - is_active (boolean)                                        │
│  - role_id (UUID foreign key)                                 │
│  - company_id (UUID foreign key)                              │
│  - created_at, updated_at (timestamps)                        │
│                                                               │
│  Roles Table:                                                 │
│  - id (UUID primary key)                                      │
│  - name (varchar)                                             │
│  - description (text)                                         │
│  - is_active (boolean)                                        │
│                                                               │
│  Companies Table:                                             │
│  - id (UUID primary key)                                      │
│  - name (varchar)                                             │
│  - rfc (varchar)                                              │
│  - is_active (boolean)                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## Flujos Detallados

### 1. Flujo de Registro

```
Cliente
   │
   ├─ POST /auth/register
   │  └─ Body: {username, email, password, role_id, company_id}
   │
   ▼
FastAPI Endpoint (register())
   │
   ├─ 1. Validate DTO (Pydantic)
   │     └─ EmailStr validation
   │     └─ UUID validation
   │
   ├─ 2. Call RegisterUserUseCase.execute()
   │     │
   │     ├─ 2.1. validate_auth_credentials()
   │     │       ├─ PasswordValidator.validate()
   │     │       │  └─ Check: min 8 chars, uppercase, lowercase, digit, special
   │     │       │  └─ If invalid: raise InvalidPasswordException → 400
   │     │       │
   │     │       ├─ UsernameValidator.validate()
   │     │       │  └─ Check: 3-50 chars, valid chars, no leading digit
   │     │       │  └─ If invalid: raise InvalidUsernameException → 400
   │     │       │
   │     │       └─ EmailValidator.is_valid()
   │     │          └─ Check: basic format
   │     │          └─ If invalid: raise InvalidEmailException → 400
   │     │
   │     ├─ 2.2. Check email uniqueness
   │     │        └─ Query: SELECT * FROM users WHERE email = ?
   │     │        └─ If exists: raise UserAlreadyExistsException → 409
   │     │
   │     ├─ 2.3. Hash password
   │     │        └─ hash_password(password)
   │     │        └─ Uses bcrypt with 10 rounds
   │     │
   │     ├─ 2.4. Create user in DB
   │     │        └─ INSERT INTO users (...)
   │     │        └─ is_active = True
   │     │        └─ Return: User entity
   │     │
   │     └─ 2.5. Auto-login (create JWT token)
   │            └─ Call LoginUserUseCase.execute()
   │            └─ create_access_token(data, expires_delta)
   │            └─ Token contains: sub, email, username, role_id, company_id, is_active
   │
   ├─ 3. Return TokenDTO
   │     └─ access_token, token_type, user_id, username, email, role_id, is_active
   │
   └─ 4. HTTP 201 Created
      └─ Client stores access_token
```

---

### 2. Flujo de Login

```
Cliente
   │
   ├─ POST /auth/login
   │  └─ Body: {email, password}
   │
   ▼
FastAPI Endpoint (login())
   │
   ├─ 1. Validate DTO (Pydantic)
   │     └─ EmailStr validation
   │
   ├─ 2. Call LoginUserUseCase.execute()
   │     │
   │     ├─ 2.1. Query user by email
   │     │        └─ SELECT * FROM users WHERE email = ?
   │     │        └─ If not found:
   │     │           └─ Log: "Email no existe: {email}"
   │     │           └─ Raise InvalidCredentialsException → 401
   │     │
   │     ├─ 2.2. Verify password
   │     │        └─ verify_password(password, user.password_hash)
   │     │        └─ Uses bcrypt comparison
   │     │        └─ If incorrect:
   │     │           └─ Log: "Contraseña incorrecta: {email}"
   │     │           └─ Raise InvalidCredentialsException → 401
   │     │
   │     ├─ 2.3. Check user is active
   │     │        └─ IF NOT user.is_active:
   │     │           └─ Log: "Usuario inactivo: {email}"
   │     │           └─ Raise UserInactiveException → 403
   │     │
   │     ├─ 2.4. Create JWT token
   │     │        └─ Token data:
   │     │           {
   │     │             "sub": user.id_user,
   │     │             "username": user.username,
   │     │             "email": user.email,
   │     │             "role_id": user.role_id,
   │     │             "company_id": user.company_id,
   │     │             "is_active": user.is_active
   │     │           }
   │     │        └─ create_access_token(data, expires_delta=30min)
   │     │        └─ Algorithm: HS256
   │     │        └─ Secret: SECRET_KEY from .env
   │     │
   │     └─ 2.5. Log success
   │            └─ Log: "Login exitoso: {email}"
   │
   ├─ 3. Return TokenDTO
   │     └─ access_token, token_type, user_id, ...
   │
   └─ 4. HTTP 200 OK
      └─ Client stores access_token in Authorization header
```

---

### 3. Flujo de Acceso a Recurso Protegido

```
Cliente
   │
   ├─ GET /api/users/me
   │  └─ Header: Authorization: Bearer <access_token>
   │
   ▼
FastAPI oauth2_scheme
   │
   ├─ 1. Extract token from header
   │     └─ "Bearer <access_token>" → extract <access_token>
   │
   ▼
Dependency: get_current_user()
   │
   ├─ 1. Decode token
   │     └─ decode_token(token)
   │     └─ Uses jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
   │     └─ If invalid/corrupted:
   │        └─ Raise InvalidTokenException → 401
   │     └─ If expired:
   │        └─ Catch ExpiredSignatureError
   │        └─ Raise TokenExpiredException → 401
   │
   ├─ 2. Validate required fields
   │     └─ Check payload contains: sub, email, username, role_id, company_id, is_active
   │     └─ If missing:
   │        └─ Log: "Token inválido: campos faltantes"
   │        └─ Raise InvalidTokenException → 401
   │
   ├─ 3. Validate user is active
   │     └─ If NOT payload["is_active"]:
   │        └─ Log: "Usuario inactivo en token"
   │        └─ Raise UserInactiveException → 403
   │
   └─ 4. Return payload dict
      └─ current_user = {sub, email, username, role_id, company_id, is_active}
```

---

### 4. Flujo de Control de Acceso (Role-Based)

```
Cliente
   │
   ├─ GET /api/admin/users
   │  └─ Header: Authorization: Bearer <admin_token>
   │  └─ Expected: user with role_id = ADMIN_ROLE_ID
   │
   ▼
FastAPI Endpoint (with require_admin dependency)
   │
   ├─ 1. Call require_admin()
   │     │
   │     ├─ 1.1. First call get_current_user()
   │     │       └─ (Same as above - validate token)
   │     │       └─ return current_user dict
   │     │
   │     ├─ 1.2. Extract role_id from payload
   │     │        └─ role_id = current_user.get("role_id")
   │     │
   │     ├─ 1.3. Compare with ADMIN_ROLE_ID
   │     │        └─ if str(role_id) != ADMIN_ROLE_ID:
   │     │           └─ Log: "Intento acceso admin sin permisos: {user_id}"
   │     │           └─ Raise InsufficientPermissionsException → 403
   │     │
   │     └─ 1.4. Return current_user
   │            └─ Handler is guaranteed user is admin
   │
   ├─ 2. Handler executes with current_user available
   │     └─ Can access: current_user["sub"], ["email"], ["role_id"], etc
   │
   └─ 3. HTTP 200 OK
      └─ Admin data returned
```

---

## Estructura de Directorios

```
app/
│
├── core/                                    ← CORE LAYER
│   ├── __init__.py
│   ├── security.py                          ← Password hashing, JWT
│   ├── validators.py                        ← Input validation
│   ├── exceptions.py                        ← Custom exceptions
│   └── middleware/
│       └── auth_middleware.py               ← JWT middleware, role checks
│
├── application/                             ← APPLICATION LAYER
│   ├── dto/
│   │   └── auth_dto/
│   │       ├── __init__.py
│   │       └── auth_dto.py                  ← RegisterDTO, LoginDTO, TokenDTO
│   │
│   └── use_cases/
│       └── auth_case/
│           ├── __init__.py
│           ├── register_user.py             ← Registration use case
│           └── login_user.py                ← Login use case
│
├── domain/                                  ← DOMAIN LAYER
│   ├── entities/
│   │   └── user_model.py                    ← User entity
│   │
│   └── ports/
│       └── out/
│           └── user_repository.py           ← Repository interface
│
└── infrastructure/                          ← INFRASTRUCTURE LAYER
    ├── adapters/
    │   └── into/
    │       └── http/
    │           ├── __init__.py
    │           └── auth.py                  ← FastAPI endpoints
    │
    ├── db/
    │   ├── engine.py
    │   ├── session.py
    │   └── models/
    │       └── user_orm.py                  ← ORM User model
    │
    └── config/
        ├── __init__.py
        ├── dependencies.py                  ← General dependencies
        └── auth_dependencies.py             ← Auth dependencies
```

---

## Componentes y Responsabilidades

### 1. Core Layer (`app/core/`)

**security.py:**
- Password hashing/verification (bcrypt)
- JWT token creation/validation
- Token expiration checks
- Responsibilities: Cryptography, token management

**validators.py:**
- Password strength validation
- Email format validation
- Username format validation
- Responsibilities: Input validation rules

**exceptions.py:**
- Custom exception hierarchy
- Error codes and default messages
- Responsibilities: Error definitions

**middleware/auth_middleware.py:**
- JWT token extraction
- User authentication
- Role-based authorization
- Responsibilities: Request authentication, authorization

---

### 2. Application Layer (`app/application/`)

**use_cases/auth_case/register_user.py:**
- Registration orchestration
- Credential validation
- User creation
- Responsibilities: Business logic for user registration

**use_cases/auth_case/login_user.py:**
- Login orchestration
- Credential verification
- Token generation
- Responsibilities: Business logic for user authentication

**dto/auth_dto/auth_dto.py:**
- Request/response models
- Pydantic validation
- Responsibilities: Data transfer object definitions

---

### 3. Domain Layer (`app/domain/`)

**entities/user_model.py:**
- User entity definition
- User properties and state
- Responsibilities: Domain model representation

**ports/out/user_repository.py:**
- Repository interface
- Abstract persistence operations
- Responsibilities: Define what the domain needs from infrastructure

---

### 4. Infrastructure Layer (`app/infrastructure/`)

**adapters/into/http/auth.py:**
- FastAPI endpoints
- HTTP request handling
- Exception to HTTP conversion
- Responsibilities: HTTP protocol handling

**db/models/user_orm.py:**
- ORM model mapping
- Database schema
- Responsibilities: Database persistence

**config/auth_dependencies.py:**
- Dependency injection configuration
- Use case instantiation
- Repository injection
- Responsibilities: Object composition

---

## Data Flow Examples

### Example 1: Register Success

```
1. Client: POST /auth/register
2. FastAPI: validate_request_body() → RegisterDTO
3. Endpoint: register_user_use_case.execute(...)
4. UseCase: validate_auth_credentials() → OK
5. UseCase: get_user_by_email(email) → None
6. UseCase: hash_password(password)
7. UseCase: create_user() → User
8. UseCase: create_access_token()
9. UseCase: return {access_token, ...}
10. Endpoint: return TokenDTO
11. FastAPI: HTTP 201 Created
12. Client: stores access_token
```

### Example 2: Login with Invalid Password

```
1. Client: POST /auth/login
2. FastAPI: validate_request_body() → LoginDTO
3. Endpoint: login_user_use_case.execute(email, password)
4. UseCase: get_user_by_email(email) → User found
5. UseCase: verify_password(password, hash) → False
6. UseCase: raise InvalidCredentialsException()
7. Endpoint: catch InvalidCredentialsException
8. Endpoint: raise HTTPException(401, "Invalid email or password")
9. FastAPI: HTTP 401 Unauthorized
10. Client: shows error to user
```

### Example 3: Protected Route Access

```
1. Client: GET /api/users/me with Authorization header
2. FastAPI: extract token from Authorization header
3. Middleware: get_current_user()
4. Security: decode_token(token)
5. Security: return payload
6. Middleware: validate payload fields
7. Middleware: return current_user dict
8. Endpoint: handler receives current_user
9. Endpoint: can access current_user["sub"], ["email"], etc
10. Endpoint: return user data
11. FastAPI: HTTP 200 OK
12. Client: receives user data
```

---

## Error Handling Flow

```
Client Request
    │
    ├─ Invalid input (DTO validation)
    │  └─ Pydantic ValidationError → HTTPException(422)
    │
    ├─ Registration error
    │  ├─ UserAlreadyExistsException → HTTPException(409)
    │  └─ InvalidPasswordException → HTTPException(400)
    │
    ├─ Login error
    │  ├─ InvalidCredentialsException → HTTPException(401)
    │  └─ UserInactiveException → HTTPException(403)
    │
    ├─ Protected route error
    │  ├─ InvalidTokenException → HTTPException(401)
    │  ├─ TokenExpiredException → HTTPException(401)
    │  └─ UserInactiveException → HTTPException(403)
    │
    ├─ Permission error
    │  └─ InsufficientPermissionsException → HTTPException(403)
    │
    └─ Unexpected error
       └─ Generic Exception → HTTPException(500)
```

---

## Security Implementation

### Authentication
```
Password Hashing:
  password → bcrypt(rounds=10) → hash_stored_in_db

Password Verification:
  password + hash → bcrypt.checkpw() → True/False

Token Generation:
  user_data → JWT(algorithm=HS256, secret=SECRET_KEY, exp=30min) → token

Token Validation:
  token → JWT.decode(secret=SECRET_KEY) → payload or exception
```

### Authorization
```
Role-Based Access Control:
  current_user.role_id == ADMIN_ROLE_ID → allow admin perms
  current_user.role_id in [ADMIN_ROLE_ID, OBSERVER_ROLE_ID] → allow observer perms
```

### Input Validation
```
Password:
  length >= 8 AND has_upper AND has_lower AND has_digit AND has_special

Username:
  3 <= length <= 50 AND matches_pattern AND not_starts_with_digit

Email:
  format_valid (done by Pydantic EmailStr)
```

---

## Logging Points

```
Core/Security:
  - DEBUG: Token created with payload
  - DEBUG: Token decoded successfully
  - WARNING: token decode failed
  - ERROR: Unexpected crypto error

Middleware:
  - INFO: Token validation initiated
  - WARNING: Invalid/expired token
  - WARNING: User not active
  - WARNING: Insufficient permissions

Use Cases:
  - INFO: Registration/Login started
  - WARNING: Validation failed
  - WARNING: User not found
  - WARNING: Duplicate email
  - INFO: User created/authenticated successfully

Endpoints:
  - INFO: Request received with email
  - WARNING: Error type and context
  - ERROR: Unexpected error
```

---

Este diagrama arquitectónico proporciona una vista completa de cómo el sistema de autenticación está estructurado y cómo los datos fluyen a través de las diferentes capas.

