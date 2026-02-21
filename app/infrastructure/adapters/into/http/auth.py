from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.application.dto.auth_dto.auth_dto import (
    RegisterDTO, LoginDTO, TokenDTO, CurrentUserDTO, ErrorResponseDTO
)
from app.application.use_cases.auth_case.register_user import RegisterUserUseCase
from app.application.use_cases.auth_case.login_user import LoginUserUseCase
from app.infrastructure.config.auth_dependencies import (
    get_register_user_use_case,
    get_login_user_use_case
)
from app.core.middleware.auth_middleware import get_current_user
from app.core.exceptions import (
    InvalidPasswordException,
    InvalidEmailException,
    InvalidUsernameException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserInactiveException
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=TokenDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponseDTO, "description": "Error en el registro"},
        409: {"model": ErrorResponseDTO, "description": "Usuario ya existe"}
    }
)
def register(
    register_dto: RegisterDTO,
    register_user_use_case: RegisterUserUseCase = Depends(get_register_user_use_case)
):
    """
    Registra un nuevo usuario con contraseña hasheada.
    
    - **username**: nombre de usuario (3-50 caracteres)
    - **email**: email único
    - **password**: contraseña (mínimo 8 caracteres)
    - **role_id**: UUID del rol
    - **company_id**: UUID de la company
    """
    try:
        logger.info(f"Intento de registro para: {register_dto.email}")
        
        user = register_user_use_case.execute(
            username=register_dto.username,
            email=register_dto.email,
            password=register_dto.password,
            role_id=str(register_dto.role_id),
            company_id=str(register_dto.company_id)
        )
        
        # Crear y retornar token automáticamente después del registro
        from app.application.use_cases.auth_case.login_user import LoginUserUseCase
        
        login_use_case = LoginUserUseCase(register_user_use_case.user_repository)
        token_data = login_use_case.execute(
            email=register_dto.email,
            password=register_dto.password
        )
        
        logger.info(f"Usuario registrado exitosamente: {register_dto.email}")
        
        return TokenDTO(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            user_id=token_data["user_id"],
            username=token_data["username"],
            email=token_data["email"],
            role_id=token_data["role_id"],
            is_active=token_data["is_active"]
        )
    except UserAlreadyExistsException as e:
        logger.error(f"Usuario ya existe: {register_dto.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.default_message
        )
    except (InvalidPasswordException, InvalidUsernameException, InvalidEmailException) as e:
        logger.warning(f"Validación fallida en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred during registration"
        )


@router.post(
    "/login",
    response_model=TokenDTO,
    responses={
        401: {"model": ErrorResponseDTO, "description": "Credenciales inválidas"},
        403: {"model": ErrorResponseDTO, "description": "Usuario inactivo"}
    }
)
def login(
    login_dto: LoginDTO,
    login_user_use_case: LoginUserUseCase = Depends(get_login_user_use_case)
):
    """
    Autentica un usuario y retorna un JWT token.
    
    - **email**: email del usuario
    - **password**: contraseña del usuario
    
    El token retornado debe incluirse en el header:
    `Authorization: Bearer <access_token>`
    """
    try:
        logger.info(f"Intento de login para: {login_dto.email}")
        
        token_data = login_user_use_case.execute(
            email=login_dto.email,
            password=login_dto.password
        )
        
        logger.info(f"Login exitoso para: {login_dto.email}")
        
        return TokenDTO(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            user_id=token_data["user_id"],
            username=token_data["username"],
            email=token_data["email"],
            role_id=token_data["role_id"],
            is_active=token_data["is_active"]
        )
    except UserInactiveException as e:
        logger.warning(f"Usuario inactivo intenta login: {login_dto.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    except (InvalidCredentialsException, Exception) as e:
        logger.warning(f"Fallo en login para {login_dto.email}: credenciales inválidas")
        # No revelar si el usuario existe o no por seguridad
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.get(
    "/me",
    response_model=CurrentUserDTO,
    responses={
        401: {"model": ErrorResponseDTO, "description": "Token inválido o expirado"},
        403: {"model": ErrorResponseDTO, "description": "Usuario inactivo"}
    }
)
def get_current_user_info(payload: dict = Depends(get_current_user)):
    """
    Obtiene la información del usuario actual basado en el JWT token.
    
    Requiere autenticación via JWT token en el header:
    `Authorization: Bearer <access_token>`
    """
    logger.info(f"Obtención de información de usuario: {payload.get('sub')}")
    
    return CurrentUserDTO(
        user_id=payload.get("sub"),
        username=payload.get("username"),
        email=payload.get("email"),
        role_id=payload.get("role_id"),
        company_id=payload.get("company_id"),
        is_active=payload.get("is_active")
    )


@router.post("/validate-token")
def validate_token(payload: dict = Depends(get_current_user)):
    """
    Valida que el token JWT sea válido y el usuario esté activo.
    
    Retorna:
    - 200: Token válido
    - 401: Token inválido o expirado
    - 403: Usuario inactivo
    """
    return {
        "valid": True,
        "user_id": payload.get("sub"),
        "username": payload.get("username"),
        "message": "Token is valid"
    }
