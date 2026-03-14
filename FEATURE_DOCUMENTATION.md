"""
PROCESO-BASED INVENTORY MANAGEMENT SYSTEM - FEATURE DOCUMENTATION
==================================================================

OVERVIEW
--------
This new feature replaces the legacy warehouse/location-based stock model with 
a process-based inventory tracking system. Products now flow through defined 
processes (production, loan, storage, disposal) with real-time alert generation 
for critical stock levels.

ARCHITECTURE PATTERN
--------------------
Hexagonal Architecture Layer Separation:
- Domain Layer: Business logic and entities
- Application Layer: Use cases orchestrating domain operations
- Infrastructure Layer: Data persistence and external integrations

ENTITIES
--------

1. PROCESS (Proceso)
   Purpose: Defines the contexts where products flow
   
   Fields:
   - id_proceso (PK): Auto-increment integer
   - nombre: Process name (max 100 chars)
   - descripcion: Optional description (max 500 chars)
   - tipo_proceso: ENUM - 'produccion', 'prestamo', 'almacenamiento', 'descarte'
   - id_empresa: Foreign key to Company (multi-tenant)
   - is_active: Boolean flag for soft deletes
   - created_at/updated_at: Automatic timestamps
   
   Types Explained:
   - 'produccion': Manufacturing/production area
   - 'prestamo': Loan/temporary use context
   - 'almacenamiento': Storage/warehouse location
   - 'descarte': Disposal/waste management
   
   Example:
   {
     "id_proceso": 1,
     "nombre": "Producción Química",
     "descripcion": "Línea de producción principal",
     "tipo_proceso": "produccion",
     "id_empresa": "uuid-company-1",
     "is_active": true,
     "created_at": "2025-03-01T10:00:00",
     "updated_at": "2025-03-01T10:00:00"
   }


2. PRODUCT MOVEMENT (Movimiento de Producto)
   Purpose: Tracks product flows between processes with complete audit trail
   
   Fields:
   - id_movimiento (PK): Auto-increment integer
   - codigo_producto: FK to Product
   - id_proceso_origen: FK to Process (source context)
   - id_proceso_destino: FK to Process (destination context)
   - cantidad: Quantity moved (positive float)
   - notas: Optional movement notes (max 500 chars)
   - id_empresa: FK to Company (multi-tenant)
   - estado: ENUM - 'pendiente', 'en_transito', 'completado', 'cancelado'
   - created_at/updated_at: Automatic timestamps
   
   State Lifecycle:
   - pendiente: Movement initiated
   - en_transito: Product in transit
   - completado: Delivery confirmed
   - cancelado: Movement cancelled
   
   Example:
   {
     "id_movimiento": 1,
     "codigo_producto": "CHEM001",
     "id_proceso_origen": 1,
     "id_proceso_destino": 2,
     "cantidad": 25.5,
     "notas": "Transferred to loan process",
     "id_empresa": "uuid-company-1",
     "estado": "completado",
     "created_at": "2025-03-01T10:00:00",
     "updated_at": "2025-03-01T10:30:00"
   }


3. CHEMICAL STOCK (Stock Químico)
   Purpose: Real-time inventory tracking with automatic alert thresholds
   
   Fields:
   - id_stock_quimico (PK): Auto-increment integer
   - codigo_producto: FK to Product
   - id_proceso: FK to Process (which process holds this stock)
   - cantidad_actual: Current inventory quantity
   - cantidad_minima: Threshold for critical alerts
   - cantidad_maxima: Capacity/maximum allowed
   - unidad_medida: Unit (ml, g, l, kg, etc)
   - id_empresa: FK to Company
   - is_active: Boolean flag
   - created_at/updated_at: Automatic timestamps
   
   Smart Properties (Computed):
   - es_stock_critico: bool = (cantidad_actual < cantidad_minima)
   - es_stock_bajo: bool = (cantidad_actual < cantidad_minima * 0.5 AND !es_stock_critico)
   - porcentaje_stock: float = (cantidad_actual / cantidad_maxima) * 100
   
   These properties enable DDD: the entity knows its state and can trigger decisions
   
   Example:
   {
     "id_stock_quimico": 1,
     "codigo_producto": "CHEM001",
     "id_proceso": 1,
     "cantidad_actual": 45.0,
     "cantidad_minima": 50.0,
     "cantidad_maxima": 200.0,
     "unidad_medida": "ml",
     "id_empresa": "uuid-company-1",
     "is_active": true,
     "es_stock_critico": false,
     "es_stock_bajo": true,
     "porcentaje_stock": 22.5,
     "created_at": "2025-03-01T10:00:00",
     "updated_at": "2025-03-01T10:00:00"
   }


4. STOCK ALERT (Alerta de Stock)
   Purpose: Real-time notifications when inventory thresholds are crossed
   
   Fields:
   - id_alerta (PK): Auto-increment integer
   - codigo_producto: FK to Product
   - id_proceso: FK to Process
   - id_stock_quimico: FK to ChemicalStock (optional, for relationship tracking)
   - tipo_alerta: ENUM - 'stock_critico', 'stock_bajo', 'exceso'
   - cantidad_actual: Current quantity at alert time
   - cantidad_referencia: Reference threshold (min/max depending on type)
   - id_empresa: FK to Company
   - estado: ENUM - 'activa', 'resuelta', 'ignorada'
   - descripcion: Alert details (max 500 chars)
   - resolved_at: Timestamp of resolution (NULL if not resolved)
   - created_at/updated_at: Automatic timestamps
   
   Alert Types:
   - 'stock_critico': Quantity < minimum threshold (URGENT)
   - 'stock_bajo': Quantity < 50% of minimum (WARNING)
   - 'exceso': Quantity > maximum capacity (OVERFLOW)
   
   Lifecycle:
   - activa: Alert is current and requires action
   - resuelta: Alert has been addressed (sets resolved_at timestamp)
   - ignorada: Alert dismissed without action
   
   Example:
   {
     "id_alerta": 1,
     "codigo_producto": "CHEM001",
     "id_proceso": 1,
     "tipo_alerta": "stock_critico",
     "cantidad_actual": 8.5,
     "cantidad_referencia": 50.0,
     "id_empresa": "uuid-company-1",
     "estado": "activa",
     "descripcion": "Critical level reached: 8.5ml < 50ml minimum",
     "resolved_at": null,
     "created_at": "2025-03-01T10:00:00",
     "updated_at": "2025-03-01T10:00:00"
   }


API ENDPOINTS
=============

PROCESS MANAGEMENT
-------------------

GET /processes/
  Query: company_id (string)
  Returns: List[ProcessResponseDTO]
  Description: Get all processes for company
  Status: 200 OK

GET /processes/{id_proceso}
  Query: company_id
  Path: id_proceso (int)
  Returns: ProcessResponseDTO
  Status: 200 OK or 404 Not Found

POST /processes/
  Body: ProcessCreateDTO
  Returns: ProcessResponseDTO
  Status: 201 Created
  Fields: nombre, descripcion, tipo_proceso, id_empresa

PUT /processes/{id_proceso}
  Path: id_proceso (int)
  Body: ProcessUpdateDTO (optional fields)
  Returns: ProcessResponseDTO
  Status: 200 OK or 400 Bad Request

DELETE /processes/{id_proceso}
  Query: company_id
  Path: id_proceso (int)
  Status: 204 No Content or 404 Not Found


PRODUCT MOVEMENT MANAGEMENT
----------------------------

GET /movements/
  Query: company_id
  Returns: List[ProductMovementResponseDTO]
  Description: Get all movements
  Status: 200 OK

GET /movements/{id_movimiento}
  Query: company_id
  Path: id_movimiento (int)
  Returns: ProductMovementResponseDTO
  Status: 200 OK or 404 Not Found

POST /movements/
  Body: ProductMovementCreateDTO
  Returns: ProductMovementResponseDTO
  Status: 201 Created
  AutoTrigger: Creates StockAlert if destination stock crosses thresholds
  Fields: codigo_producto, id_proceso_origen, id_proceso_destino, cantidad, notas, id_empresa

PUT /movements/{id_movimiento}
  Path: id_movimiento (int)
  Body: ProductMovementUpdateDTO (optional fields)
  Returns: ProductMovementResponseDTO
  Status: 200 OK

PATCH /movements/{id_movimiento}/status
  Path: id_movimiento (int)
  Query: nuevo_estado (pendiente|en_transito|completado|cancelado)
  Returns: ProductMovementResponseDTO
  Status: 200 OK or 400 Bad Request

DELETE /movements/{id_movimiento}
  Query: company_id
  Path: id_movimiento (int)
  Status: 204 No Content


CHEMICAL STOCK MANAGEMENT
--------------------------

GET /stocks/
  Query: company_id
  Returns: List[ChemicalStockResponseDTO]
  Description: Get all chemical stocks
  Status: 200 OK

GET /stocks/critical
  Query: company_id
  Returns: List[ChemicalStockResponseDTO]
  Description: Dashboard - Get only critical stocks (cantidad_actual < cantidad_minima)
  Status: 200 OK
  UseCase: Centralized view of items needing immediate attention

GET /stocks/{id_stock_quimico}
  Query: company_id
  Path: id_stock_quimico (int)
  Returns: ChemicalStockResponseDTO (includes computed properties)
  Status: 200 OK

POST /stocks/
  Body: ChemicalStockCreateDTO
  Returns: ChemicalStockResponseDTO
  Status: 201 Created
  Fields: codigo_producto, id_proceso, cantidad_actual, cantidad_minima, cantidad_maxima, unidad_medida, id_empresa

PUT /stocks/{id_stock_quimico}
  Path: id_stock_quimico (int)
  Body: ChemicalStockUpdateDTO (optional fields)
  Returns: ChemicalStockResponseDTO
  Status: 200 OK

DELETE /stocks/{id_stock_quimico}
  Query: company_id
  Path: id_stock_quimico (int)
  Status: 204 No Content


STOCK ALERT MANAGEMENT
-----------------------

GET /alerts/
  Query: company_id
  Returns: List[StockAlertResponseDTO]
  Description: Get all alerts (all states)
  Status: 200 OK

GET /alerts/active
  Query: company_id
  Returns: List[StockAlertResponseDTO]
  Description: Dashboard - Get only active alerts (estado='activa')
  Status: 200 OK
  UseCase: Real-time alert monitoring dashboard

GET /alerts/{id_alerta}
  Query: company_id
  Path: id_alerta (int)
  Returns: StockAlertResponseDTO
  Status: 200 OK

POST /alerts/
  Body: StockAlertCreateDTO
  Returns: StockAlertResponseDTO
  Status: 201 Created
  Fields: codigo_producto, id_proceso, tipo_alerta, cantidad_actual, cantidad_referencia, id_empresa, descripcion

PUT /alerts/{id_alerta}
  Path: id_alerta (int)
  Body: StockAlertUpdateDTO (estado, descripcion)
  Returns: StockAlertResponseDTO
  Status: 200 OK

PATCH /alerts/{id_alerta}/resolve
  Path: id_alerta (int)
  Returns: StockAlertResponseDTO
  Status: 200 OK
  Action: Marks estado='resuelta' and sets resolved_at=now()

DELETE /alerts/{id_alerta}
  Query: company_id
  Path: id_alerta (int)
  Status: 204 No Content


WORKFLOW EXAMPLES
=================

SCENARIO 1: Chemical Production with Low Stock Alert
----------------------------------------------------
1. Company creates chemicalStock:
   POST /stocks/
   {
     "codigo_producto": "CHEM001",
     "id_proceso": 1,
     "cantidad_actual": 100,
     "cantidad_minima": 50,
     "cantidad_maxima": 200,
     "unidad_medida": "ml",
     "id_empresa": "company-123"
   }
   Response: 201 Created

2. Product moves to loan process:
   POST /movements/
   {
     "codigo_producto": "CHEM001",
     "id_proceso_origen": 1,
     "id_proceso_destino": 2,
     "cantidad": 60,
     "notas": "Loaned to external lab",
     "id_empresa": "company-123"
   }
   Response: 201 Created
   Action: System checks destination stock = 100 - 60 = 40
   Trigger: Creates StockAlert tipo_alerta='stock_critico' (40 < 50)

3. Check critical stocks:
   GET /stocks/critical?company_id=company-123
   Response: List includes CHEM001 with es_stock_critico=true

4. Check active alerts:
   GET /alerts/active?company_id=company-123
   Response: List shows alert estado='activa'

5. Resolve alert after restocking:
   PATCH /alerts/1/resolve
   Response: 200 OK, resolved_at timestamp set, estado='resuelta'


SCENARIO 2: Inventory Dashboard Monitoring
-------------------------------------------
1. Get critical stocks (items needing attention):
   GET /stocks/critical?company_id=company-123
   Returns all ChemicalStock where es_stock_critico=true
   
2. Get active alerts (real-time notifications):
   GET /alerts/active?company_id=company-123
   Returns all active alerts for dashboard display
   
3. Filter by type:
   GET /alerts/?company_id=company-123&estado=activa&tipo_alerta=stock_critico
   Shows only critical alerts for urgent items


IMPLEMENTATION NOTES
====================

KEY DESIGN DECISIONS:
1. Domain-Driven Design:
   - ChemicalStock entity knows its state (es_stock_critico property)
   - No separate "status calculator" service needed
   - Business logic lives in domain layer

2. Automatic Alert Generation:
   - ProductMovement creation triggers alert logic
   - CreateMovementUseCase checks destination stock thresholds
   - No manual alert creation needed in typical workflow

3. Multi-Tenant Architecture:
   - All entities have id_empresa FK
   - API accepts company_id in queries
   - Data isolation enforced at repository level

4. Soft Deletes:
   - is_active boolean flag (vs hard deletes)
   - Preserves audit trail
   - Empty recycle bin functionality possible

5. State Machines:
   - ProductMovement.estado: pendiente → en_transito → completado | cancelado
   - StockAlert.estado: activa → resuelta | ignorada
   - Explicit state transitions prevent invalid operations


DATABASE SCHEMA
===============

CREATE TABLE procesos (
  id_proceso SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(500),
  tipo_proceso VARCHAR(50) NOT NULL,
  id_empresa UUID NOT NULL REFERENCES companies(id_company),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movimientos_productos (
  id_movimiento SERIAL PRIMARY KEY,
  codigo_producto VARCHAR(50) NOT NULL REFERENCES products(id_product),
  id_proceso_origen INTEGER NOT NULL REFERENCES procesos(id_proceso),
  id_proceso_destino INTEGER NOT NULL REFERENCES procesos(id_proceso),
  cantidad FLOAT NOT NULL,
  notas VARCHAR(500),
  id_empresa UUID NOT NULL REFERENCES companies(id_company),
  estado VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_quimicos (
  id_stock_quimico SERIAL PRIMARY KEY,
  codigo_producto VARCHAR(50) NOT NULL REFERENCES products(id_product),
  id_proceso INTEGER NOT NULL REFERENCES procesos(id_proceso),
  cantidad_actual FLOAT NOT NULL DEFAULT 0,
  cantidad_minima FLOAT NOT NULL,
  cantidad_maxima FLOAT NOT NULL,
  unidad_medida VARCHAR(20) NOT NULL,
  id_empresa UUID NOT NULL REFERENCES companies(id_company),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alertas_stock (
  id_alerta SERIAL PRIMARY KEY,
  codigo_producto VARCHAR(50) NOT NULL REFERENCES products(id_product),
  id_proceso INTEGER NOT NULL REFERENCES procesos(id_proceso),
  id_stock_quimico INTEGER REFERENCES stock_quimicos(id_stock_quimico),
  tipo_alerta VARCHAR(50) NOT NULL,
  cantidad_actual FLOAT NOT NULL,
  cantidad_referencia FLOAT NOT NULL,
  id_empresa UUID NOT NULL REFERENCES companies(id_company),
  estado VARCHAR(50) NOT NULL,
  descripcion VARCHAR(500),
  resolved_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


TESTING GUIDE
=============

Example Flow with curl/Postman:

1. Create Process:
   POST http://localhost:8000/processes/
   {
     "nombre": "Production Line A",
     "descripcion": "Main production facility",
     "tipo_proceso": "produccion",
     "id_empresa": "your-company-uuid"
   }
   Note: Save id_proceso (e.g., 1)

2. Create Chemical Stock:
   POST http://localhost:8000/stocks/
   {
     "codigo_producto": "PROD001",
     "id_proceso": 1,
     "cantidad_actual": 100,
     "cantidad_minima": 50,
     "cantidad_maxima": 200,
     "unidad_medida": "ml",
     "id_empresa": "your-company-uuid"
   }
   Note: Save id_stock_quimico

3. View all stocks:
   GET http://localhost:8000/stocks/?company_id=your-company-uuid

4. View critical stocks (should be empty):
   GET http://localhost:8000/stocks/critical?company_id=your-company-uuid

5. Create process of different type:
   POST http://localhost:8000/processes/
   {
     "nombre": "Storage B",
     "tipo_proceso": "almacenamiento",
     "id_empresa": "your-company-uuid"
   }
   Note: Save process ID (e.g., 2)

6. Create movement (triggers alert generation):
   POST http://localhost:8000/movements/
   {
     "codigo_producto": "PROD001",
     "id_proceso_origen": 1,
     "id_proceso_destino": 2,
     "cantidad": 60,
     "notas": "Transfer to storage",
     "id_empresa": "your-company-uuid"
   }
   Expected: Stock becomes 40 (critical, < 50)
   Expected: StockAlert created automatically

7. View critical stocks (should show product):
   GET http://localhost:8000/stocks/critical?company_id=your-company-uuid

8. View active alerts:
   GET http://localhost:8000/alerts/active?company_id=your-company-uuid

9. Resolve alert:
   PATCH http://localhost:8000/alerts/1/resolve

10. Verify alert is resolved:
    GET http://localhost:8000/alerts/1?company_id=your-company-uuid
    Note: estado='resuelta', resolved_at is populated


FILE STRUCTURE
==============

Domain Layer:
  app/domain/entities/
    - process_model.py
    - product_movement_model.py
    - chemical_stock_model.py
    - stock_alert_model.py
  
  app/domain/ports/out/
    - process_repository.py
    - product_movement_repository.py
    - chemical_stock_repository.py
    - stock_alert_repository.py

Application Layer:
  app/application/dto/
    - process_dto/
    - product_movement_dto/
    - chemical_stock_dto/
    - stock_alert_dto/
  
  app/application/use_cases/
    - process_case/
    - product_movement_case/
    - chemical_stock_case/
    - stock_alert_case/

Infrastructure Layer:
  app/infrastructure/db/models/
    - process_orm.py
    - product_movement_orm.py
    - chemical_stock_orm.py
    - stock_alert_orm.py
  
  app/infrastructure/adapters/out/
    - process_repository_orm.py
    - product_movement_repository_orm.py
    - chemical_stock_repository_orm.py
    - stock_alert_repository_orm.py
  
  app/infrastructure/adapters/into/http/
    - processes.py
    - product_movements.py
    - chemical_stocks.py
    - stock_alerts.py
  
  app/infrastructure/config/
    - process_dependencies.py
    - product_movement_dependencies.py
    - chemical_stock_dependencies.py
    - stock_alert_dependencies.py


FUTURE ENHANCEMENTS
===================

1. Batch Alert Resolution:
   PATCH /alerts/batch/resolve
   {
     "alert_ids": [1, 2, 3],
     "company_id": "uuid"
   }

2. Historical Analytics:
   GET /movements/history?company_id=uuid&date_from=X&date_to=Y

3. Predictive Alerts:
   Based on movement velocity suggest restocking

4. Alert Escalation:
   Auto-escalate unresolved critical alerts after N hours

5. Email Notifications:
   Send alerts via email to configured recipients

6. WebSocket Real-time Updates:
   Live dashboard updates on new alerts

7. Audit Log:
   Track who resolved alerts and when

8. Batch Movements:
   Create multiple movements in single transaction

9. Custom Thresholds per Company:
   Global vs per-company alert levels

10. Export Capabilities:
    CSV export of critical stocks and alerts
"""
