"""
Use case para crear un nuevo stock químico
"""
import logging
from app.domain.entities.chemical_stock_model import ChemicalStock
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository
from app.application.dto.chemical_stock_dto import ChemicalStockCreateDTO

logger = logging.getLogger(__name__)


class CreateStockUseCase:
    """Caso de uso para crear un nuevo stock químico"""
    
    def __init__(self, stock_repository: ChemicalStockRepository):
        self.stock_repository = stock_repository
    
    def execute(self, stock_dto: ChemicalStockCreateDTO) -> ChemicalStock:
        """
        Ejecuta el caso de uso
        
        Args:
            stock_dto: DTO con los datos del stock
            
        Returns:
            Stock creado
            
        Raises:
            ValueError: Si la cantidad máxima es menor a la mínima
        """
        logger.info(f"Creando nuevo stock para producto {stock_dto.codigo_producto}")
        
        if stock_dto.cantidad_minima > stock_dto.cantidad_maxima:
            logger.error("La cantidad mínima no puede ser mayor a la máxima")
            raise ValueError("cantidad_minima no puede ser mayor a cantidad_maxima")
        
        stock = ChemicalStock(
            codigo_producto=stock_dto.codigo_producto,
            id_proceso=stock_dto.id_proceso,
            cantidad_actual=stock_dto.cantidad_actual,
            cantidad_minima=stock_dto.cantidad_minima,
            cantidad_maxima=stock_dto.cantidad_maxima,
            unidad_medida=stock_dto.unidad_medida,
            id_empresa=stock_dto.id_empresa,
            is_active=True
        )
        
        created_stock = self.stock_repository.create_stock(stock)
        logger.info(f"Stock creado exitosamente con ID {created_stock.id_stock_quimico}")
        return created_stock
