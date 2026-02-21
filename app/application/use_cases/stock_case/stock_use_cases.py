"""
Use cases para Stock (Ubicación y Almacén)
"""
from typing import List
from app.domain.ports.out.stock_location_repository import StockLocationRepository
from app.domain.ports.out.stock_warehouse_repository import StockWarehouseRepository
from app.domain.entities.stock_location_model import StockLocation
from app.domain.entities.stock_warehouse_model import StockWarehouse
import logging

logger = logging.getLogger(__name__)


# Stock Location Use Cases
class CreateStockLocationUseCase:
    """Use case para crear stock en ubicación"""
    
    def __init__(self, stock_location_repository: StockLocationRepository):
        self.stock_location_repository = stock_location_repository
    
    def execute(
        self,
        id_ubicacion: int,
        codigo_producto: str,
        cantidad: int,
        id_empresa: str
    ) -> StockLocation:
        """Crea un nuevo stock en ubicación"""
        logger.info(f"Creando stock: ubicación={id_ubicacion}, producto={codigo_producto}")
        
        stock = StockLocation(
            id_ubicacion=id_ubicacion,
            codigo_producto=codigo_producto,
            cantidad=cantidad,
            id_empresa=id_empresa
        )
        
        created = self.stock_location_repository.create_stock(stock)
        logger.info(f"Stock creado exitosamente")
        return created


class GetStockLocationsUseCase:
    """Use case para obtener stocks por ubicación"""
    
    def __init__(self, stock_location_repository: StockLocationRepository):
        self.stock_location_repository = stock_location_repository
    
    def get_all(self, company_id: str) -> List[StockLocation]:
        """Obtiene todos los stocks"""
        return self.stock_location_repository.get_all_stocks(company_id)
    
    def get_by_location(self, location_id: int, company_id: str) -> List[StockLocation]:
        """Obtiene stocks de una ubicación"""
        return self.stock_location_repository.get_stocks_by_location(location_id, company_id)
    
    def get_by_product(self, product_code: str, company_id: str) -> List[StockLocation]:
        """Obtiene ubicaciones de un producto"""
        return self.stock_location_repository.get_stocks_by_product(product_code, company_id)


class UpdateStockLocationUseCase:
    """Use case para actualizar stock en ubicación"""
    
    def __init__(self, stock_location_repository: StockLocationRepository):
        self.stock_location_repository = stock_location_repository
    
    def execute(
        self,
        id_ubicacion: int,
        codigo_producto: str,
        stock: StockLocation
    ) -> StockLocation:
        """Actualiza un stock"""
        logger.info(f"Actualizando stock: ubicación={id_ubicacion}, producto={codigo_producto}")
        updated = self.stock_location_repository.update_stock(id_ubicacion, codigo_producto, stock)
        if not updated:
            raise Exception(f"Could not update stock")
        return updated


class DeleteStockLocationUseCase:
    """Use case para eliminar stock en ubicación"""
    
    def __init__(self, stock_location_repository: StockLocationRepository):
        self.stock_location_repository = stock_location_repository
    
    def execute(self, location_id: int, product_code: str, company_id: str) -> bool:
        """Elimina un stock"""
        logger.info(f"Eliminando stock: ubicación={location_id}, producto={product_code}")
        deleted = self.stock_location_repository.delete_stock(location_id, product_code, company_id)
        if not deleted:
            raise Exception(f"Could not delete stock")
        return True


# Stock Warehouse Use Cases
class CreateStockWarehouseUseCase:
    """Use case para crear stock en almacén"""
    
    def __init__(self, stock_warehouse_repository: StockWarehouseRepository):
        self.stock_warehouse_repository = stock_warehouse_repository
    
    def execute(
        self,
        codigo_producto: str,
        cantidad: int,
        id_empresa: str
    ) -> StockWarehouse:
        """Crea un stock en almacén"""
        logger.info(f"Creando stock almacén: {codigo_producto}")
        
        stock = StockWarehouse(
            codigo_producto=codigo_producto,
            cantidad=cantidad,
            id_empresa=id_empresa
        )
        
        created = self.stock_warehouse_repository.create_stock(stock)
        logger.info(f"Stock almacén creado")
        return created


class GetStockWarehousesUseCase:
    """Use case para obtener stocks del almacén"""
    
    def __init__(self, stock_warehouse_repository: StockWarehouseRepository):
        self.stock_warehouse_repository = stock_warehouse_repository
    
    def get_all(self, company_id: str) -> List[StockWarehouse]:
        """Obtiene todos los stocks del almacén"""
        return self.stock_warehouse_repository.get_all_stocks(company_id)
    
    def get_by_product(self, product_code: str, company_id: str) -> StockWarehouse:
        """Obtiene el stock de un producto"""
        stock = self.stock_warehouse_repository.get_stock_by_product(product_code, company_id)
        if not stock:
            raise Exception(f"Stock for product {product_code} not found")
        return stock


class UpdateStockWarehouseUseCase:
    """Use case para actualizar stock en almacén"""
    
    def __init__(self, stock_warehouse_repository: StockWarehouseRepository):
        self.stock_warehouse_repository = stock_warehouse_repository
    
    def execute(self, codigo_producto: str, stock: StockWarehouse) -> StockWarehouse:
        """Actualiza un stock"""
        logger.info(f"Actualizando stock almacén: {codigo_producto}")
        updated = self.stock_warehouse_repository.update_stock(codigo_producto, stock)
        if not updated:
            raise Exception(f"Could not update stock")
        return updated
    
    def increment(self, product_code: str, quantity: int, company_id: str) -> StockWarehouse:
        """Incrementa el stock"""
        logger.info(f"Incrementando stock: {product_code} +{quantity}")
        stock = self.stock_warehouse_repository.increment_stock(product_code, quantity, company_id)
        if not stock:
            raise Exception(f"Could not increment stock")
        return stock
    
    def decrement(self, product_code: str, quantity: int, company_id: str) -> StockWarehouse:
        """Decrementa el stock"""
        logger.info(f"Decrementando stock: {product_code} -{quantity}")
        stock = self.stock_warehouse_repository.decrement_stock(product_code, quantity, company_id)
        if not stock:
            raise Exception(f"Could not decrement stock")
        return stock


class DeleteStockWarehouseUseCase:
    """Use case para eliminar stock en almacén"""
    
    def __init__(self, stock_warehouse_repository: StockWarehouseRepository):
        self.stock_warehouse_repository = stock_warehouse_repository
    
    def execute(self, product_code: str, company_id: str) -> bool:
        """Elimina un stock"""
        logger.info(f"Eliminando stock almacén: {product_code}")
        deleted = self.stock_warehouse_repository.delete_stock(product_code, company_id)
        if not deleted:
            raise Exception(f"Could not delete stock")
        return True
