"""
Pruebas y ejemplos para entender el flujo de autenticación
"""

# EJEMPLO 1: Cómo se hashea una contraseña
# ==================================================

from app.core.security import hash_password, verify_password

# Cuando un usuario se registra:
password_plain = "micontraseña123"
password_hashed = hash_password(password_plain)
# password_hashed = $2b$12$... (hash bcrypt único cada vez)

# Cuando un usuario hace login:
password_input = "micontraseña123"
is_valid = verify_password(password_input, password_hashed)
# is_valid = True

password_wrong = "contraseña_incorrecta"
is_valid = verify_password(password_wrong, password_hashed)
# is_valid = False


# EJEMPLO 2: Cómo se crean y validan los tokens JWT
# ==================================================

from app.core.security import create_access_token, decode_token, get_user_from_token
from datetime import timedelta

# Cuando un usuario hace login:
user_data = {
    "sub": "550e8400-e29b-41d4-a716-446655440000",  # user_id
    "username": "john",
    "role_id": "550e8400-e29b-41d4-a716-446655440000",  # admin role
    "company_id": "550e8400-e29b-41d4-a716-446655440002"
}

token = create_access_token(data=user_data, expires_delta=timedelta(minutes=30))
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Cuando una petición llega con el token:
payload = decode_token(token)
# payload = {"sub": "550e8400...", "username": "john", ...}

user_id = get_user_from_token(token)
# user_id = "550e8400-e29b-41d4-a716-446655440000"


# EJEMPLO 3: Flujo completo de autenticación
# ==================================================

# 1. REGISTRO
"""
POST /auth/register
{
  "username": "john",
  "email": "john@example.com",
  "password": "segurpassword123",
  "role_id": "550e8400-e29b-41d4-a716-446655440000",  # admin
  "company_id": "550e8400-e29b-41d4-a716-446655440002"
}

- hash_password("segurpassword123") → $2b$12$...
- Guardar usuario con contraseña hasheada en BD
- Automáticamente se crea y retorna un token JWT
"""

# 2. LOGIN
"""
POST /auth/login
{
  "email": "john@example.com",
  "password": "segurpassword123"
}

- Buscar usuario por email en BD
- verify_password("segurpassword123", hash_de_bd) → True
- create_access_token() → JWT con expiración
- Retornar token
"""

# 3. USAR EL TOKEN
"""
GET /users/
Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

- decode_token(token) → payload con datos del usuario
- Verificar que el token sea válido y no haya expirado
- Verificar el role_id si es necesario
- Permitir o denegar acceso según los permisos
"""


# EJEMPLO 4: Validación de roles en middlewares
# ==================================================

"""
@router.delete("/{user_id}")
def delete_user(..., payload: dict = Depends(require_admin)):
    # require_admin verifica que role_id == ADMIN_ROLE_ID
    # Si el usuario es observador, retorna 403 Forbidden
    # Si el usuario es admin, permite continuar
"""

# Middlewares disponibles:
# - get_current_user(): Requiere autenticación cualquier usuario
# - require_admin(): Requiere rol de administrador
# - require_observer(): Requiere rol de observador o administrador
