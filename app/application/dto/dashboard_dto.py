from pydantic import BaseModel
from typing import List, Dict

class ProcessStockStat(BaseModel):
    process_id: str
    process_name: str
    total_stock: float
    percentage: float

class DashboardStatsDTO(BaseModel):
    total_products: int
    low_stock_alerts: int
    movements_today: int
    active_processes: int
    stock_by_process: List[ProcessStockStat]
