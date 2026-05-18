from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from uuid import UUID
import pandas as pd
import io
import logging
from sqlalchemy.orm import Session
from app.application.dto.products_dto.product_dto import ProductDTO
from app.application.dto.products_dto.create_product_dto import CreateProductDTO
from app.application.dto.products_dto.update_product_dto import UpdateProductDTO
from app.application.use_cases.products_case.get_all_products import GetAllProductsUseCase
from app.application.use_cases.products_case.get_product_by_id import GetProductByIdUseCase
from app.application.use_cases.products_case.get_products_by_company_id import GetProductsByCompanyIdUseCase
from app.application.use_cases.products_case.create_product import CreateProductUseCase
from app.application.use_cases.products_case.update_product import UpdateProductUseCase
from app.application.use_cases.products_case.delete_product import DeleteProductUseCase
from app.infrastructure.config.products_dependencies import (
    get_all_products_use_case,
    get_product_by_id_use_case,
    get_products_by_company_id_use_case,
    get_create_product_use_case,
    get_update_product_use_case,
    get_delete_product_use_case
)
from app.infrastructure.db.session import get_session
from app.core.middleware.auth_middleware import (
    get_current_user,
    require_admin,
    require_company_admin
)
from app.domain.entities.product_model import Product
from fastapi.responses import StreamingResponse
from app.application.services.report_service import ReportService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])

# --- Column mapping: Excel header (Spanish) → Product field ---
TEMPLATE_COLUMNS = [
    "codigo",
    "nombre",
    "cantidad",
    "nombre_generico",
    "unidad_medida",
    "limite_critico",
    "fds"
]

REQUIRED_COLUMNS = {"codigo", "nombre", "cantidad"}


def require_company_admin_or_global_admin():
    """
    Returns a dependency that checks:
    - Global admin OR
    - Company admin for the user's company
    """
    async def check(
        payload: dict = Depends(get_current_user)
    ):
        from app.settings import settings
        role_id = payload.get("role_id")
        user_company_id = payload.get("company_id")
        
        # Global admin can do anything
        if role_id == settings.ADMIN_ROLE_ID:
            return payload
        
        # Check if company admin
        company_admin_role = f"company_admin_{user_company_id}"
        if role_id == company_admin_role:
            return payload
        
        # Also allow old style if it starts with company_admin_
        if str(role_id).startswith("company_admin_"):
            return payload
        
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return check


# ──────────────────────────────────────────────
# Bulk-upload helpers
# ──────────────────────────────────────────────

@router.get("/bulk-template")
def download_bulk_template(
    payload: dict = Depends(require_company_admin_or_global_admin())
):
    """
    Descarga una plantilla Excel vacía con las columnas esperadas para la carga masiva.
    Solo administradores de la compañía pueden descargarla.
    """
    df = pd.DataFrame(columns=TEMPLATE_COLUMNS)
    # Add one example row so the user understands the format
    example = {
        "codigo": "A00000001",
        "nombre": "SODA EN ESCAMAS",
        "cantidad": 100,
        "nombre_generico": "HIDROXIDO DE SODIO",
        "unidad_medida": "KG",
        "limite_critico": 10.0,
        "fds": "X",
    }
    df = pd.concat([df, pd.DataFrame([example])], ignore_index=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Productos")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=plantilla_productos.xlsx"},
    )


@router.post("/bulk-upload")
def bulk_upload_products(
    file: UploadFile = File(...),
    create_product_use_case: CreateProductUseCase = Depends(get_create_product_use_case),
    update_product_use_case: UpdateProductUseCase = Depends(get_update_product_use_case),
    get_product_by_id_use_case: GetProductByIdUseCase = Depends(get_product_by_id_use_case),
    session: Session = Depends(get_session),
    payload: dict = Depends(require_company_admin_or_global_admin()),
):
    """
    Carga masiva de productos desde un archivo Excel (.xlsx).
    Procesa todas las hojas del Excel. Cada hoja representa una bodega.
    Si el producto ya existe (mismo id_product), se actualiza.
    Solo administradores de la compañía pueden usar este endpoint.
    """
    if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx)")

    user_company_id = payload.get("company_id")
    if not user_company_id:
        raise HTTPException(status_code=400, detail="No se pudo determinar la compañía del usuario")

    try:
        contents = file.file.read()
        xl = pd.ExcelFile(io.BytesIO(contents))
    except Exception as e:
        logger.error(f"Error al leer el archivo Excel: {e}")
        raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo Excel: {str(e)}")

    company_uuid = UUID(str(user_company_id))
    processed_count = 0
    errors = []

    from app.infrastructure.db.models.process_orm import ProcessORM
    from app.infrastructure.db.models.provider_orm import ProviderORM
    from app.infrastructure.db.models.product_provider_orm import ProductProviderORM
    from app.infrastructure.db.models.stock_orm import StockWarehouseORM
    import uuid

    for sheet_name in xl.sheet_names:
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name)
        except Exception as e:
            errors.append({"sheet": sheet_name, "error": f"No se pudo leer la hoja: {str(e)}"})
            continue

        if df.empty:
            continue

        # Normalize columns: lower and stripped
        df.columns = [str(c).strip().lower() for c in df.columns]

        # Resolve mandatory columns dynamically
        id_col = None
        name_col = None
        qty_col = None

        for col in df.columns:
            if col in ["codigo", "código", "id_product", "id product", "code", "cod"]:
                id_col = col
            elif col in ["nombre", "name", "nombre del producto", "descripcion", "descripción", "item"]:
                name_col = col
            elif col in ["cantidad", "quantity", "cant", "qty", "total inven", "total invent", "unnamed: 2", "total"]:
                qty_col = col

        if not id_col or not name_col or not qty_col:
            # Skip this sheet if it doesn't contain mandatory columns
            logger.info(f"Hoja '{sheet_name}' omitida por falta de columnas obligatorias")
            continue

        # Resolve optional columns dynamically
        generic_col = next((c for c in df.columns if c in ["generic_name", "generic name", "nombre generico", "nombre genérico", "uso de la sustancia"]), None)
        price_col = next((c for c in df.columns if c in ["price", "precio"]), None)
        unit_measure_col = next((c for c in df.columns if c in ["unit_measure", "unit measure", "unidad de medida", "unid", "unidad"]), None)
        unit_price_col = next((c for c in df.columns if c in ["unit_price", "unit price", "precio unitario", "precio_unitario"]), None)
        min_unit_price_col = next((c for c in df.columns if c in ["min_unit_price", "min unit price", "precio_minimo", "precio minimo"]), None)
        lead_time_col = next((c for c in df.columns if c in ["lead_time_days", "lead time days", "dias entrega", "días entrega"]), None)
        restorage_col = next((c for c in df.columns if c in ["restorage", "almacenamiento", "estado fisico", "estado físico", "tipo de envase"]), None)
        limite_critico_col = next((c for c in df.columns if c in ["limite_critico", "limite critico", "límite crítico", "limite_critico_stock"]), None)
        fds_col = next((c for c in df.columns if c in ["fds", "ficha de seguridad", "ficha_seguridad"]), None)
        provider_col = next((c for c in df.columns if c in ["proveedor", "proveedor principal", "proveedor_principal"]), None)

        # Get or create warehouse for this sheet
        warehouse_name = str(sheet_name).strip()
        warehouse = session.query(ProcessORM).filter(
            ProcessORM.id_empresa == company_uuid,
            ProcessORM.nombre == warehouse_name,
            ProcessORM.tipo_proceso == "almacenamiento"
        ).first()

        if not warehouse:
            warehouse = ProcessORM(
                id_proceso=uuid.uuid4(),
                nombre=warehouse_name,
                descripcion=f"Bodega importada automáticamente de la hoja {warehouse_name}",
                tipo_proceso="almacenamiento",
                id_empresa=company_uuid,
                is_active=True
            )
            session.add(warehouse)
            session.commit()
            session.refresh(warehouse)

        # Process each row
        for idx, row in df.iterrows():
            row_num = idx + 2
            try:
                id_product = str(row.get(id_col, "")).strip()
                name = str(row.get(name_col, "")).strip()
                
                # Parse quantity
                cantidad = 0
                raw_qty = row.get(qty_col, 0)
                if pd.notna(raw_qty):
                    try:
                        cantidad = int(float(raw_qty))
                    except (ValueError, TypeError):
                        pass

                if not id_product or not name:
                    errors.append({"sheet": sheet_name, "row": row_num, "error": "Código o Nombre vacíos"})
                    continue

                # Parse optional fields
                generic_name = str(row.get(generic_col, "")).strip() if generic_col else ""
                unit_measure = str(row.get(unit_measure_col, "UNIDAD")).strip() if unit_measure_col else "UNIDAD"
                
                # Numeric parsing helpers
                def parse_float(val):
                    if pd.isna(val) or str(val).strip() == "":
                        return 0.0
                    try:
                        return float(val)
                    except ValueError:
                        return 0.0

                def parse_int(val):
                    if pd.isna(val) or str(val).strip() == "":
                        return 0
                    try:
                        return int(float(val))
                    except ValueError:
                        return 0

                price = parse_float(row.get(price_col)) if price_col else 0.0
                unit_price = parse_float(row.get(unit_price_col)) if unit_price_col else 0.0
                min_unit_price = parse_float(row.get(min_unit_price_col)) if min_unit_price_col else 0.0
                lead_time_days = parse_int(row.get(lead_time_col)) if lead_time_col else 0
                restorage = str(row.get(restorage_col, "")).strip() if restorage_col else ""
                limite_critico = parse_float(row.get(limite_critico_col)) if limite_critico_col else 0.0
                fds = str(row.get(fds_col, "")).strip() if fds_col else ""
                
                provider_name = str(row.get(provider_col, "")).strip() if provider_col else ""

                existing = get_product_by_id_use_case.execute(id_product)

                if existing:
                    product_data = {
                        "name": name,
                        "generic_name": generic_name or existing.generic_name,
                        "price": price or existing.price,
                        "unit_measure": unit_measure or existing.unit_measure,
                        "unit_price": unit_price or existing.unit_price,
                        "min_unit_price": min_unit_price or existing.min_unit_price,
                        "lead_time_days": lead_time_days or existing.lead_time_days,
                        "restorage": restorage or existing.restorage,
                        "limite_critico": limite_critico or existing.limite_critico,
                        "warehouse_id": warehouse.id_proceso,
                        "fds": fds or existing.fds,
                    }
                    update_product_use_case.execute(id_product, product_data)
                else:
                    product = Product(
                        id_product=id_product,
                        name=name,
                        generic_name=generic_name,
                        price=price,
                        unit_measure=unit_measure,
                        unit_price=unit_price,
                        min_unit_price=min_unit_price,
                        lead_time_days=lead_time_days,
                        restorage=restorage,
                        limite_critico=limite_critico,
                        warehouse_id=warehouse.id_proceso,
                        company_id=company_uuid,
                        fds=fds,
                        fds_url=None
                    )
                    create_product_use_case.execute(product)

                # Write or update Stock Warehouse record
                stock_record = session.query(StockWarehouseORM).filter(
                    StockWarehouseORM.codigo_producto == id_product,
                    StockWarehouseORM.id_empresa == company_uuid
                ).first()
                if stock_record:
                    stock_record.cantidad = cantidad
                else:
                    stock_record = StockWarehouseORM(
                        codigo_producto=id_product,
                        cantidad=cantidad,
                        id_empresa=company_uuid
                    )
                    session.add(stock_record)
                
                # Check and link provider if specified
                if provider_name:
                    db_prov = session.query(ProviderORM).filter(
                        ProviderORM.id_empresa == company_uuid,
                        (ProviderORM.nombre.ilike(provider_name) | ProviderORM.cad_proveedor.ilike(provider_name))
                    ).first()
                    if db_prov:
                        existing_rel = session.query(ProductProviderORM).filter(
                            ProductProviderORM.codigo_producto == id_product,
                            ProductProviderORM.cad_proveedor == db_prov.cad_proveedor
                        ).first()
                        if not existing_rel:
                            prov_rel = ProductProviderORM(
                                codigo_producto=id_product,
                                cad_proveedor=db_prov.cad_proveedor,
                                es_principal=True,
                                precio=unit_price
                            )
                            session.add(prov_rel)

                processed_count += 1

            except Exception as e:
                session.rollback()
                errors.append({"sheet": sheet_name, "row": row_num, "error": str(e)})

    # Commit all warehouse stocks and providers
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos en base de datos: {str(e)}")

    return {
        "message": f"Carga masiva completada: {processed_count} productos procesados ({len(errors)} errores)",
        "created": processed_count,
        "errors": errors,
    }


# ──────────────────────────────────────────────
# Standard CRUD endpoints
# ──────────────────────────────────────────────

@router.get("/", response_model=list[ProductDTO], dependencies=[Depends(get_current_user)])
def get_all_products(
    get_all_products_use_case: GetAllProductsUseCase = Depends(get_all_products_use_case),
    payload: dict = Depends(get_current_user)
):
    """
    Lista todos los productos (requiere autenticación)
    """
    products = get_all_products_use_case.execute()
    return [ProductDTO.from_entity(product) for product in products]

@router.get("/by-id/{product_id}", response_model=ProductDTO, dependencies=[Depends(get_current_user)])
def get_product_by_id(
    product_id: str,
    get_product_by_id_use_case: GetProductByIdUseCase = Depends(get_product_by_id_use_case),
    payload: dict = Depends(get_current_user)
):
    """
    Obtiene un producto por ID (requiere autenticación)
    """
    product = get_product_by_id_use_case.execute(product_id)
    if product is None:
        return {"error": "Product not found"}
    return ProductDTO.from_entity(product)

@router.get("/by-company/{company_id}", response_model=list[ProductDTO], dependencies=[Depends(get_current_user)])
def get_products_by_company_id(
    company_id: UUID,
    get_products_by_company_id_use_case: GetProductsByCompanyIdUseCase = Depends(get_products_by_company_id_use_case),
    payload: dict = Depends(get_current_user)
):
    """
    Obtiene productos por company ID (solo accesibles para members de esa company)
    """
    user_company_id = payload.get("company_id")
    
    # Check user can only access their own company data
    if str(company_id) != str(user_company_id):
        raise HTTPException(status_code=403, detail="Access denied to this company's products")
    
    products = get_products_by_company_id_use_case.execute(str(company_id))
    return [ProductDTO.from_entity(product) for product in products]

@router.get("/by-company/{company_id}/export/excel", dependencies=[Depends(get_current_user)])
def export_products_excel(
    company_id: UUID,
    get_products_by_company_id_use_case: GetProductsByCompanyIdUseCase = Depends(get_products_by_company_id_use_case),
    payload: dict = Depends(get_current_user)
):
    """
    Exporta los productos de una empresa en formato Excel (solo admins de esa company)
    """
    user_company_id = payload.get("company_id")
    
    if str(company_id) != str(user_company_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    products = get_products_by_company_id_use_case.execute(str(company_id))
    data = [ProductDTO.from_entity(p).model_dump() for p in products]
    
    excel_file = ReportService.generate_excel(data)
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=productos.xlsx"}
    )

@router.post("/", response_model=ProductDTO)
def create_product(
    create_product_dto: CreateProductDTO,
    create_product_use_case: CreateProductUseCase = Depends(get_create_product_use_case),
    payload: dict = Depends(require_company_admin_or_global_admin())
):
    """
    Crea un nuevo producto (requiere rol de admin de la company)
    """
    from uuid import UUID
    warehouse_uuid = None
    if create_product_dto.warehouse_id:
        warehouse_uuid = UUID(str(create_product_dto.warehouse_id))
    
    product = create_product_use_case.execute(Product(
        id_product=create_product_dto.id_product,
        name=create_product_dto.name,
        generic_name=create_product_dto.generic_name,
        price=create_product_dto.price,
        unit_measure=create_product_dto.unit_measure,
        unit_price=create_product_dto.unit_price,
        min_unit_price=create_product_dto.min_unit_price,
        lead_time_days=create_product_dto.lead_time_days,
        restorage=create_product_dto.restorage,
        limite_critico=create_product_dto.limite_critico,
        warehouse_id=warehouse_uuid,
        company_id=create_product_dto.company_id
    ))
    return ProductDTO.from_entity(product)

@router.put("/{product_id}", response_model=ProductDTO)
def update_product(
    product_id: str,
    update_product_dto: UpdateProductDTO,
    update_product_use_case: UpdateProductUseCase = Depends(get_update_product_use_case),
    payload: dict = Depends(require_company_admin_or_global_admin())
):
    """
    Actualiza un producto (requiere rol de admin de la company)
    """
    product_data = update_product_dto.model_dump(exclude_unset=True)
    product = update_product_use_case.execute(product_id, product_data)
    return ProductDTO.from_entity(product)

@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    delete_product_use_case: DeleteProductUseCase = Depends(get_delete_product_use_case),
    payload: dict = Depends(require_company_admin_or_global_admin())
):
    """
    Elimina un producto (requiere rol de admin de la company)
    """
    delete_product_use_case.execute(product_id)
    return {"message": "Product deleted successfully"}
