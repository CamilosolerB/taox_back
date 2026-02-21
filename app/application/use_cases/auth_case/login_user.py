from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User
from app.core.security import verify_password, create_access_token
from app.core.exceptions import (
    InvalidCredentialsException,
    UserInactiveException
)
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> dict:
        """
        Autentica un usuario validando:
        - Que el usuario exista
        - Que la contraseña sea correcta
        - Que el usuario esté activo
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            Diccionario con access_token, token_type y datos del usuario
            
        Raises:
            InvalidCredentialsException: Si email no existe o contraseña es incorrecta
            UserInactiveException: Si el usuario está inactivo
        """
        # Buscar el usuario por email
        user = self.user_repository.get_user_by_email(email)
        
        if user is None:
            logger.warning(f"Intento de login con email no existente: {email}")
            raise InvalidCredentialsException()
        
        # Verificar la contraseña primero
        if not verify_password(password, user.password):
            logger.warning(f"Contraseña incorrecta para usuario: {email}")
            raise InvalidCredentialsException()
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            logger.warning(f"Intento de login con usuario inactivo: {email}")
            raise UserInactiveException()
        
        # Crear el token JWT con información del usuario
        token_data = {
            "sub": str(user.id_user),
            "username": user.username,
            "email": user.email,
            "role_id": str(user.role_id),
            "company_id": str(user.company_id),
            "is_active": user.is_active
        }
        
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=30)
        )
        
        logger.info(f"Login exitoso para usuario: {email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id_user,
            "username": user.username,
            "email": user.email,
            "role_id": user.role_id,
            "is_active": user.is_active
        }
