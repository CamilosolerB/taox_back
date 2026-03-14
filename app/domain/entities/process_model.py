"""
Entidad de Dominio para Proceso
"""
from uuid import UUID, uuid4
from datetime import datetime


class Process:
    """Representa un proceso en el sistema (producción, préstamo, etc)"""
    
    def __init__(
        self,
        nombre: str,
        descripcion: str,
        tipo_proceso: str,  # 'produccion', 'prestamo', 'almacenamiento', 'descarte'
        id_empresa: UUID,
        id_proceso: UUID = None,
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id_proceso = id_proceso or uuid4()
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo_proceso = tipo_proceso
        self.id_empresa = id_empresa
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def __repr__(self):
        return f"Process(id={self.id_proceso}, nombre='{self.nombre}', tipo='{self.tipo_proceso}')"
