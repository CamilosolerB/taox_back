"""
Use case para obtener un stock químico por ID
"""
import logging
from app.domain.entities.chemical_stock_model import ChemicalStock
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository

logger = logging.getLogger(__name__)


class GetStockByIdUseCase:
    """Caso de uso para obtener un stock químico por ID"""
    
    def __init__(self, stock_repository: ChemicalStockRepository):
        self.stock_repository = stock_repository
    
    def execute(self, id_stock_quimico: int, company_id: str) -> ChemicalStock:
        """
        Ejecuta el caso de uso
        
        Args:
            id_stock_quimico: ID del stock
            company_id: ID de la empresa
            
        Returns:
            Stock encontrado
            
        Raises:
            ValueError: Si el stock no existe
        """
        logger.info(f"Obteniendo stock {id_stock_quimico} de la empresa {company_id}")
        stock = self.stock_repository.get_stock_by_id(id_stock_quimico, company_id)
        if not stock:
            logger.error(f"Stock {id_stock_quimico} no encontrado")
            raise ValueError(f"Stock con ID {id_stock_quimico} no existe")
        return stock
