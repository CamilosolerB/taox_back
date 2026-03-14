"""
Use case para obtener stocks críticos
"""
import logging
from typing import List
from app.domain.entities.chemical_stock_model import ChemicalStock
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository

logger = logging.getLogger(__name__)


class GetCriticalStocksUseCase:
    """Caso de uso para obtener todos los stocks críticos"""
    
    def __init__(self, stock_repository: ChemicalStockRepository):
        self.stock_repository = stock_repository
    
    def execute(self, company_id: str) -> List[ChemicalStock]:
        """
        Ejecuta el caso de uso
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de stocks en nivel crítico
        """
        logger.info(f"Obteniendo stocks críticos para la empresa {company_id}")
        critical_stocks = self.stock_repository.get_critical_stocks(company_id)
        logger.info(f"Se encontraron {len(critical_stocks)} stocks críticos")
        return critical_stocks
