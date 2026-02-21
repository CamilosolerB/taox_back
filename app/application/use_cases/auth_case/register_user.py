from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User
from app.core.security import hash_password
from app.core.validators import validate_auth_credentials
from app.core.exceptions import (
    InvalidPasswordException,
    InvalidEmailException,
    InvalidUsernameException,
    UserAlreadyExistsException
)
import logging

logger = logging.getLogger(__name__)


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, email: str, password: str, role_id: str, company_id: str) -> User:
        """
        Registra un nuevo usuario validando:
        - Que el usuario no exista (email único)
        - Que el username sea válido
        - Que la contraseña cumpla requisitos de seguridad
        - Que el email sea válido
        
        Args:
            username: Nombre de usuario
            email: Email único del usuario
            password: Contraseña en texto plano
            role_id: UUID del rol
            company_id: UUID de la company
            
        Returns:
            Usuario creado
            
        Raises:
            InvalidPasswordException: Si la contraseña no cumple requisitos
            InvalidUsernameException: Si el nombre de usuario es inválido
            InvalidEmailException: Si el email es inválido
            UserAlreadyExistsException: Si el usuario ya existe
        """
        # Validar credenciales
        try:
            validate_auth_credentials(username, email, password)
        except (InvalidUsernameException, InvalidPasswordException, InvalidEmailException) as e:
            logger.warning(f"Validación fallida en registro: {str(e)}")
            raise
        
        # Verificar si el usuario ya existe
        if self.user_repository.get_user_by_email(email) is not None:
            logger.warning(f"Intento de registro con email ya existente: {email}")
            raise UserAlreadyExistsException()
        
        # Hash la contraseña
        hashed_password = hash_password(password)
        
        logger.info(f"Registrando nuevo usuario: {email}")
        
        # Crear el usuario
        user = User(
            id_user=None,
            username=username,
            email=email,
            password=hashed_password,
            is_active=True,
            role_id=role_id,
            company_id=company_id
        )
        
        created_user = self.user_repository.create_user(user)
        logger.info(f"Usuario registrado exitosamente: {email}")
        
        return created_user
