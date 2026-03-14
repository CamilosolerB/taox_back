"""
Use case para actualizar un stock químico
"""
import logging
from app.domain.entities.chemical_stock_model import ChemicalStock
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository
from app.application.dto.chemical_stock_dto import ChemicalStockUpdateDTO

logger = logging.getLogger(__name__)


class UpdateStockUseCase:
    """Caso de uso para actualizar un stock químico"""
    
    def __init__(self, stock_repository: ChemicalStockRepository):
        self.stock_repository = stock_repository
    
    def execute(self, id_stock_quimico: int, stock_dto: ChemicalStockUpdateDTO) -> ChemicalStock:
        """
        Ejecuta el caso de uso
        
        Args:
            id_stock_quimico: ID del stock a actualizar
            stock_dto: DTO con los datos a actualizar
            
        Returns:
            Stock actualizado
            
        Raises:
            ValueError: Si los parámetros son inválidos
        """
        logger.info(f"Actualizando stock {id_stock_quimico}")
        
        update_data = stock_dto.model_dump(exclude_unset=True)
        
        if not update_data:
            logger.warning(f"No hay campos para actualizar en stock {id_stock_quimico}")
            raise ValueError("Se debe proporcionar al menos un campo para actualizar")
        
        # Validar que cantidad_minima no sea mayor a cantidad_maxima
        if "cantidad_minima" in update_data and "cantidad_maxima" in update_data:
            if update_data["cantidad_minima"] > update_data["cantidad_maxima"]:
                logger.error("cantidad_minima no puede ser mayor a cantidad_maxima")
                raise ValueError("cantidad_minima no puede ser mayor a cantidad_maxima")
        
        updated_stock = self.stock_repository.update_stock(id_stock_quimico, update_data)
        logger.info(f"Stock {id_stock_quimico} actualizado exitosamente")
        return updated_stock
