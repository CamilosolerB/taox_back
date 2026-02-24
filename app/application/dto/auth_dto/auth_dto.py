from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class RegisterDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: EmailStr = Field(..., description="Email único del usuario")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")
    role_id: UUID = Field(..., description="ID del rol del usuario")
    company_id: UUID = Field(..., description="ID de la company del usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "SecurePass123!",
                "role_id": "550e8400-e29b-41d4-a716-446655440000",
                "company_id": "550e8400-e29b-41d4-a716-446655440002"
            }
        }


class LoginDTO(BaseModel):
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123!"
            }
        }


class TokenDTO(BaseModel):
    access_token: str = Field(..., description="JWT token para autenticación")
    token_type: str = Field(default="bearer", description="Tipo de token")
    user_id: UUID = Field(..., description="ID del usuario autenticado")
    username: str = Field(..., description="Nombre de usuario")
    email: str = Field(..., description="Email del usuario")
    role_id: UUID = Field(..., description="ID del rol")
    is_active: bool = Field(..., description="Si el usuario está activo")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "john_doe",
                "email": "john@example.com",
                "role_id": "550e8400-e29b-41d4-a716-446655440000",
                "is_active": True
            }
        }


class TokenPayloadDTO(BaseModel):
    sub: str = Field(..., description="User ID")
    username: str = Field(..., description="Nombre de usuario")
    email: str = Field(..., description="Email del usuario")
    role_id: str = Field(..., description="ID del rol")
    company_id: str = Field(..., description="ID de la company")
    is_active: bool = Field(..., description="Si el usuario está activo")


class CurrentUserDTO(BaseModel):
    user_id: str = Field(..., description="ID del usuario")
    username: str = Field(..., description="Nombre de usuario")
    email: str = Field(..., description="Email del usuario")
    role_id: str = Field(..., description="ID del rol")
    company_id: str = Field(..., description="ID de la company")
    is_active: bool = Field(..., description="Si el usuario está activo")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "john_doe",
                "email": "john@example.com",
                "role_id": "550e8400-e29b-41d4-a716-446655440000",
                "company_id": "550e8400-e29b-41d4-a716-446655440002",
                "is_active": True
            }
        }


class ErrorResponseDTO(BaseModel):
    error: str = Field(..., description="Mensaje de error")
    error_code: str = Field(..., description="Código de error")
    details: str = Field(default="", description="Detalles adicionales")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid email or password",
                "error_code": "AUTH_001",
                "details": "Las credenciales proporcionadas no son válidas"
            }
        }
