"""
Entidad de dominio para Ubicación
"""
from typing import Optional
from datetime import datetime


class Location:
    """
    Entidad Ubicación (UBICACION)
    
    Representa una ubicación en el almacén para almacenar productos.
    """
    
    def __init__(
        self,
        id_ubicacion: Optional[int] = None,
        ubicacion: str = None,
        posicion: str = None,
        nivel: str = None,
        tipo_ubicacion: str = None,
        localizador: str = None,
        id_empresa: str = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id_ubicacion = id_ubicacion
        self.ubicacion = ubicacion
        self.posicion = posicion
        self.nivel = nivel
        self.tipo_ubicacion = tipo_ubicacion
        self.localizador = localizador
        self.id_empresa = id_empresa
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"<Location {self.id_ubicacion}: {self.ubicacion}>"
