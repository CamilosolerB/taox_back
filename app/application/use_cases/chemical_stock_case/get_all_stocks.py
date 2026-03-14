"""
Use case para obtener todos los stocks químicos
"""
import logging
from typing import List
from app.domain.entities.chemical_stock_model import ChemicalStock
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository

logger = logging.getLogger(__name__)


class GetAllStocksUseCase:
    """Caso de uso para obtener todos los stocks químicos"""
    
    def __init__(self, stock_repository: ChemicalStockRepository):
        self.stock_repository = stock_repository
    
    def execute(self, company_id: str) -> List[ChemicalStock]:
        """
        Ejecuta el caso de uso
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de stocks químicos
        """
        logger.info(f"Obteniendo todos los stocks químicos para la empresa {company_id}")
        stocks = self.stock_repository.get_all_stocks(company_id)
        logger.info(f"Se encontraron {len(stocks)} stocks químicos")
        return stocks
