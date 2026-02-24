"""
Validadores específicos para autenticación
"""
from typing import Optional, Tuple
from app.core.exceptions import (
    InvalidPasswordException,
    InvalidEmailException,
    InvalidUsernameException
)


class PasswordValidator:
    """Validador de contraseñas"""
    
    MIN_LENGTH = 8
    MAX_LENGTH = 72  # Límite de bcrypt
    REQUIRES_UPPERCASE = True
    REQUIRES_LOWERCASE = True
    REQUIRES_DIGIT = True
    REQUIRES_SPECIAL = True
    
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    @classmethod
    def validate(cls, password: str) -> Tuple[bool, Optional[str]]:
        """
        Valida una contraseña según criterios de seguridad.
        
        Args:
            password: Contraseña a validar
            
        Returns:
            Tupla (válida, mensaje_error)
        """
        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters"
        
        if len(password) > cls.MAX_LENGTH:
            return False, f"Password must not exceed {cls.MAX_LENGTH} characters (bcrypt limit)"
        
        if cls.REQUIRES_UPPERCASE and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if cls.REQUIRES_LOWERCASE and not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if cls.REQUIRES_DIGIT and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        if cls.REQUIRES_SPECIAL and not any(c in cls.SPECIAL_CHARS for c in password):
            return False, f"Password must contain at least one special character: {cls.SPECIAL_CHARS}"
        
        return True, None


class EmailValidator:
    """Validador de emails (ya lo hace Pydantic con EmailStr)"""
    
    @staticmethod
    def is_valid(email: str) -> bool:
        """
        Validación básica de email (Pydantic hace lo principal)
        """
        return "@" in email and "." in email.split("@")[1]


class UsernameValidator:
    """Validador de nombres de usuario"""
    
    MIN_LENGTH = 3
    MAX_LENGTH = 50
    ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    
    @classmethod
    def validate(cls, username: str) -> Tuple[bool, Optional[str]]:
        """
        Valida un nombre de usuario.
        
        Args:
            username: Nombre de usuario a validar
            
        Returns:
            Tupla (válido, mensaje_error)
        """
        if len(username) < cls.MIN_LENGTH:
            return False, f"Username must be at least {cls.MIN_LENGTH} characters"
        
        if len(username) > cls.MAX_LENGTH:
            return False, f"Username must not exceed {cls.MAX_LENGTH} characters"
        
        if not all(c in cls.ALLOWED_CHARS for c in username):
            return False, f"Username can only contain: {cls.ALLOWED_CHARS}"
        
        if username[0].isdigit():
            return False, "Username cannot start with a number"
        
        return True, None


def validate_auth_credentials(username: str, email: str, password: str) -> None:
    """
    Valida todas las credenciales de autenticación.
    
    Lanza excepciones específicas de validación si hay algún error.
    """
    # Validar username
    valid, error = UsernameValidator.validate(username)
    if not valid:
        raise InvalidUsernameException(error)
    
    # Validar password
    valid, error = PasswordValidator.validate(password)
    if not valid:
        raise InvalidPasswordException(error)
    
    # Validar email (Pydantic lo hace en el DTO)
    if not EmailValidator.is_valid(email):
        raise InvalidEmailException()
