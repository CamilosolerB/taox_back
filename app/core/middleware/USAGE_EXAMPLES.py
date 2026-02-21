"""
Ejemplo de cómo usar los middlewares por roles en los endpoints

Reemplaza el ADMIN_ROLE_ID y OBSERVER_ROLE_ID en tu archivo .env con los UUIDs de los roles

Ejemplo de uso en endpoints:

from fastapi import APIRouter, Depends
from app.core.middleware.auth_middleware import (
    get_current_user,
    require_admin,
    require_observer
)

router = APIRouter()

# Endpoint que requiere autenticación (cualquier usuario autenticado)
@router.get("/protected")
def protected_endpoint(payload: dict = Depends(get_current_user)):
    return {"message": "Acceso permitido para usuarios autenticados", "user": payload}

# Endpoint que requiere rol de administrador
@router.delete("/{item_id}")
def delete_item(item_id: str, payload: dict = Depends(require_admin)):
    return {"message": f"Item {item_id} eliminado", "deleted_by": payload.get("username")}

# Endpoint que requiere rol de observador o administrador
@router.get("/view-reports")
def view_reports(payload: dict = Depends(require_observer)):
    return {"message": "Acceso a reportes permitido", "user": payload}

# Endpoint público (sin protección)
@router.get("/public")
def public_endpoint():
    return {"message": "Acceso público"}
"""
