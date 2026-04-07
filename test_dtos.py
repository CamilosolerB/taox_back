from uuid import uuid4
from app.application.dto.stock_alert_dto.stock_alert_dto import StockAlertCreateDTO, StockAlertResponseDTO
from app.application.dto.product_movement_dto.product_movement_dto import ProductMovementCreateDTO, ProductMovementResponseDTO
from app.application.dto.process_dto.process_dto import ProcessResponseDTO
from app.application.dto.chemical_stock_dto.chemical_stock_dto import ChemicalStockCreateDTO, ChemicalStockResponseDTO
from datetime import datetime

def test_dtos():
    mock_uuid = uuid4()
    
    # Stock Alert
    sa_res = StockAlertResponseDTO(
        id_alerta=1,
        codigo_producto="CHEM001",
        id_proceso=mock_uuid,
        tipo_alerta="bajo",
        cantidad_actual=5.0,
        cantidad_referencia=10.0,
        id_empresa="empresa-1",
        estado="activa",
        descripcion=None,
        resolved_at=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    print("StockAlertResponseDTO OK")

    # Movement
    pm_res = ProductMovementResponseDTO(
        id_movimiento=1,
        codigo_producto="CHEM001",
        id_proceso_origen=mock_uuid,
        id_proceso_destino=mock_uuid,
        tipo_movimiento="traslado",
        cantidad=10.5,
        notas=None,
        id_empresa="empresa-1",
        estado="completado",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    print("ProductMovementResponseDTO OK")

    # Process
    pr_res = ProcessResponseDTO(
        id_proceso=mock_uuid,
        nombre="Proc1",
        descripcion=None,
        tipo_proceso="produccion",
        id_empresa="empresa-1",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    print("ProcessResponseDTO OK")

if __name__ == "__main__":
    test_dtos()
    print("ALL OK")
