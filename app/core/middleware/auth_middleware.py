from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from app.core.security import decode_token_with_blacklist_check as decode_token
from typing import Optional, Dict
import logging

# Configurar logging
logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Valida el JWT token y retorna los datos del usuario.
    Verifica:
    - Token válido y no expirado
    - Token no está en blacklist
    - Usuario activo
    - Campos requeridos presentes
    """
    token = credentials.credentials
    
    # Decodificar y validar el token (con blacklist check)
    payload = decode_token(token)
    
    if payload is None:
        logger.warning(f"Intento de acceso con token inválido o expirado")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    # Validar que el usuario esté activo
    is_active = payload.get("is_active", False)
    if not is_active:
        logger.warning(f"Intento de acceso con usuario inactivo: {payload.get('sub')}")
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )
    
    # Validar que los campos requeridos estén presentes
    required_fields = ["sub", "username", "role_id", "company_id"]
    for field in required_fields:
        if field not in payload:
            logger.error(f"Token corrupto: falta campo {field}")
            raise HTTPException(
                status_code=401,
                detail="Invalid token format"
            )
    
    return payload


async def require_admin(payload: Dict = Depends(get_current_user)):
    """
    Middleware que verifica que el usuario tenga rol de administrador global
    (definido en settings.ADMIN_ROLE_ID)
    """
    from app.settings import settings
    
    role_id = payload.get("role_id")
    user_id = payload.get("sub")
    
    if role_id != settings.ADMIN_ROLE_ID:
        logger.warning(f"Intento de acceso administrativo por usuario no-admin: {user_id}")
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    
    return payload


def require_company_admin():
    """
    Dependency factory that verifies user is admin of their OWN company.
    
    The user must have a role_id that starts with "company_admin_" 
    and matches their company_id.
    """
    from app.settings import settings
    
    async def check_company_admin(
        payload: Dict = Depends(get_current_user)
    ):
        user_company_id = payload.get("company_id")
        role_id = payload.get("role_id")
        user_id = payload.get("sub")
        
        # Global admin can do anything
        if role_id == settings.ADMIN_ROLE_ID:
            return payload
        
        # Check if role is company_admin for this company
        expected_role = f"company_admin_{user_company_id}"
        
        if str(role_id) != expected_role:
            logger.warning(f"Intento de acceso {user_id} sin permisos de admin para company {user_company_id}")
            raise HTTPException(
                status_code=403,
                detail="Company admin access required"
            )
        
        return payload
    
    return check_company_admin


def require_company_member():
    """
    Dependency factory that verifies user belongs to the company
    being accessed and has access to that company's resources.
    """
    async def check_company_member(
        payload: Dict = Depends(get_current_user)
    ):
        return payload
    
    return check_company_member


async def require_observer(payload: Dict = Depends(get_current_user)):
    """
    Middleware que verifica que el usuario tenga rol de observador o administrador
    """
    from app.settings import settings
    
    role_id = payload.get("role_id")
    user_id = payload.get("sub")
    
    # Roles permitidos
    admin_role = settings.ADMIN_ROLE_ID
    observer_role = settings.OBSERVER_ROLE_ID
    
    if role_id not in [admin_role, observer_role]:
        logger.warning(f"Intento de acceso por usuario sin permisos: {user_id}")
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions"
        )
    
    return payload


def get_user_id_from_token(payload: Dict = Depends(get_current_user)) -> str:
    """
    Extrae el ID del usuario desde el payload del token
    """
    return payload.get("sub")


def get_company_id_from_token(payload: Dict = Depends(get_current_user)) -> str:
    """
    Extrae el ID de la company desde el payload del token
    """
    return payload.get("company_id")
