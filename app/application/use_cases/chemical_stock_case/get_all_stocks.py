"""
Use case para obtener todos los stocks químicos
"""
import logging
from typing import List
from uuid import UUID
from app.domain.entities.chemical_stock_model import ChemicalStock
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository

logger = logging.getLogger(__name__)


class GetAllStocksUseCase:
    def __init__(self, stock_repository: ChemicalStockRepository):
        self.stock_repository = stock_repository

    def execute(self, company_id: str, id_proceso: UUID = None) -> List[ChemicalStock]:
        """
        Ejecuta el caso de uso
        
        Args:
            company_id: ID de la empresa
            id_proceso: ID del proceso (opcional)
            
        Returns:
            Lista de stocks químicos
        """
        if id_proceso:
            logger.info(f"Obteniendo stocks químicos para empresa {company_id} y proceso {id_proceso}")
            stocks = self.stock_repository.get_stocks_by_process(id_proceso, company_id)
        else:
            logger.info(f"Obteniendo todos los stocks químicos para la empresa {company_id}")
            stocks = self.stock_repository.get_all_stocks(company_id)
            
        logger.info(f"Se encontraron {len(stocks)} stocks químicos")
        return stocks
