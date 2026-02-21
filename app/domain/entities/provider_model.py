"""
Entidad de dominio para Proveedor
"""
from typing import Optional
from datetime import datetime


class Provider:
    """
    Entidad Proveedor (PROVEEDOR)
    
    Representa un proveedor de productos en el sistema.
    """
    
    def __init__(
        self,
        cad_proveedor: str,
        nombre: str,
        contacto: str,
        direccion: str,
        telefono: str,
        celular: str,
        web: str,
        correo: str,
        id_empresa: str,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.cad_proveedor = cad_proveedor
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion
        self.telefono = telefono
        self.celular = celular
        self.web = web
        self.correo = correo
        self.id_empresa = id_empresa
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"<Provider {self.cad_proveedor}: {self.nombre}>"
