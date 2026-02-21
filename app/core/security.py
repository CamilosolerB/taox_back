from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from app.settings import settings
import logging

logger = logging.getLogger(__name__)

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """
    Hash una contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Contraseña hasheada con bcrypt
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada
        
    Returns:
        True si coinciden, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token con los datos proporcionados.
    
    Args:
        data: Datos a incluir en el token (sub, username, role_id, etc)
        expires_delta: Tiempo de expiración personalizado
        
    Returns:
        JWT token firmado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.debug(f"Token creado para usuario: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error al crear token: {str(e)}")
        raise Exception("Error al crear token de autenticación")


def decode_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un JWT token.
    
    Args:
        token: JWT token a validar
        
    Returns:
        Diccionario con los datos del token si es válido, None si no
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token decodificado exitosamente para usuario: {payload.get('sub')}")
        return payload
    except ExpiredSignatureError:
        logger.warning("Token expirado")
        return None
    except JWTError as e:
        logger.warning(f"Error de JWT: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al decodificar token: {str(e)}")
        return None


def get_user_from_token(token: str) -> Optional[str]:
    """
    Extrae el ID del usuario desde un token JWT.
    
    Args:
        token: JWT token
        
    Returns:
        ID del usuario (claim 'sub') o None si el token es inválido
    """
    payload = decode_token(token)
    if payload is None:
        return None
    return payload.get("sub")


def is_token_expired(token: str) -> bool:
    """
    Verifica si un token JWT ha expirado.
    
    Args:
        token: JWT token
        
    Returns:
        True si el token ha expirado, False si es válido
    """
    payload = decode_token(token)
    return payload is None
