"""
Entidad de dominio para Cliente
"""
from typing import Optional
from datetime import datetime


class Client:
    """
    Entidad Cliente (CLIENTE)
    
    Representa un cliente que compra productos.
    """
    
    def __init__(
        self,
        codigo_cliente: str,
        cliente: str,
        telefono1: str,
        telefono2: Optional[str],
        contacto: str,
        correo: str,
        ciudad: str,
        tipo_agua: str,
        cantidad_promedio_kg: float,
        id_empresa: str,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.codigo_cliente = codigo_cliente
        self.cliente = cliente
        self.telefono1 = telefono1
        self.telefono2 = telefono2
        self.contacto = contacto
        self.correo = correo
        self.ciudad = ciudad
        self.tipo_agua = tipo_agua
        self.cantidad_promedio_kg = cantidad_promedio_kg
        self.id_empresa = id_empresa
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"<Client {self.codigo_cliente}: {self.cliente}>"
