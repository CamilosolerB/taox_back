"""
Use case para eliminar un stock químico
"""
import logging
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository

logger = logging.getLogger(__name__)


class DeleteStockUseCase:
    """Caso de uso para eliminar un stock químico"""
    
    def __init__(self, stock_repository: ChemicalStockRepository):
        self.stock_repository = stock_repository
    
    def execute(self, id_stock_quimico: int, company_id: str) -> bool:
        """
        Ejecuta el caso de uso
        
        Args:
            id_stock_quimico: ID del stock a eliminar
            company_id: ID de la empresa
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            ValueError: Si el stock no existe
        """
        logger.info(f"Eliminando stock {id_stock_quimico} de la empresa {company_id}")
        result = self.stock_repository.delete_stock(id_stock_quimico, company_id)
        
        if not result:
            logger.error(f"No se pudo eliminar el stock {id_stock_quimico}")
            raise ValueError(f"Stock con ID {id_stock_quimico} no existe")
        
        logger.info(f"Stock {id_stock_quimico} eliminado exitosamente")
        return result
