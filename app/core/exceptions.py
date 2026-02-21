"""
Excepciones personalizadas para el módulo de autenticación
"""


class AuthenticationException(Exception):
    """Excepción base para errores de autenticación"""
    pass


class InvalidCredentialsException(AuthenticationException):
    """Excepción para credenciales inválidas"""
    error_code = "AUTH_001"
    default_message = "Invalid email or password"


class UserInactiveException(AuthenticationException):
    """Excepción para usuario inactivo"""
    error_code = "AUTH_002"
    default_message = "User account is inactive"


class UserAlreadyExistsException(AuthenticationException):
    """Excepción para usuario que ya existe"""
    error_code = "AUTH_003"
    default_message = "User with this email already exists"


class InvalidTokenException(AuthenticationException):
    """Excepción para token inválido"""
    error_code = "AUTH_004"
    default_message = "Invalid or expired token"


class TokenExpiredException(AuthenticationException):
    """Excepción para token expirado"""
    error_code = "AUTH_005"
    default_message = "Token has expired"


class InsufficientPermissionsException(AuthenticationException):
    """Excepción para permisos insuficientes"""
    error_code = "AUTH_006"
    default_message = "Insufficient permissions"


class InvalidPasswordException(AuthenticationException):
    """Excepción para contraseña inválida"""
    error_code = "AUTH_007"
    default_message = "Password does not meet security requirements"


class InvalidUsernameException(AuthenticationException):
    """Excepción para nombre de usuario inválido"""
    error_code = "AUTH_008"
    default_message = "Username does not meet requirements"


class InvalidEmailException(AuthenticationException):
    """Excepción para email inválido"""
    error_code = "AUTH_009"
    default_message = "Invalid email format"
