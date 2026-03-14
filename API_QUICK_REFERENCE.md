# INVENTORY MANAGEMENT SYSTEM - API QUICK REFERENCE

## Base URL
`http://localhost:8000`

## Endpoints Summary (24 total)

### Processes (5 endpoints)
| Method | Path | Purpose | Status |
|--------|------|---------|--------|
| GET | `/processes/` | List all processes | 200 |
| GET | `/processes/{id}` | Get process by ID | 200\|404 |
| POST | `/processes/` | Create process | 201 |
| PUT | `/processes/{id}` | Update process | 200\|400 |
| DELETE | `/processes/{id}` | Delete process | 204\|404 |

### Product Movements (6 endpoints)
| Method | Path | Purpose | Status |
|--------|------|---------|--------|
| GET | `/movements/` | List all movements | 200 |
| GET | `/movements/{id}` | Get movement by ID | 200\|404 |
| POST | `/movements/` | Create movement (⚡ triggers alerts) | 201 |
| PUT | `/movements/{id}` | Update movement | 200\|400 |
| PATCH | `/movements/{id}/status` | Update movement status | 200\|400 |
| DELETE | `/movements/{id}` | Delete movement | 204\|404 |

### Chemical Stocks (6 endpoints)
| Method | Path | Purpose | Status |
|--------|------|---------|--------|
| GET | `/stocks/` | List all stocks | 200 |
| GET | `/stocks/critical` | 📊 Dashboard - Critical stocks | 200 |
| GET | `/stocks/{id}` | Get stock by ID | 200\|404 |
| POST | `/stocks/` | Create stock | 201\|400 |
| PUT | `/stocks/{id}` | Update stock | 200\|400 |
| DELETE | `/stocks/{id}` | Delete stock | 204\|404 |

### Stock Alerts (7 endpoints)
| Method | Path | Purpose | Status |
|--------|------|---------|--------|
| GET | `/alerts/` | List all alerts | 200 |
| GET | `/alerts/active` | 📊 Active alerts (real-time) | 200 |
| GET | `/alerts/{id}` | Get alert by ID | 200\|404 |
| POST | `/alerts/` | Create alert manually | 201 |
| PUT | `/alerts/{id}` | Update alert | 200\|400 |
| PATCH | `/alerts/{id}/resolve` | Mark alert resolved | 200\|404 |
| DELETE | `/alerts/{id}` | Delete alert | 204\|404 |

## Query Parameters

Most endpoints require: `company_id` (string, UUID)

## Entity Relationships

```
Company
├── Process (defines movement contexts)
│   ├── ProductMovement (origin)
│   ├── ProductMovement (destination)
│   └── ChemicalStock → Product
│       └── StockAlert
└── Product
    ├── ProductMovement
    ├── ChemicalStock
    └── StockAlert
```

## Key Features

### 1. Automatic Alert Generation ⚡
When creating a movement:
```
POST /movements/
→ System checks destination ChemicalStock
→ If cantidad_actual < cantidad_minima: creates alert automatically
```

### 2. Smart Stock Properties
ChemicalStock includes computed properties:
- `es_stock_critico`: cantidad_actual < cantidad_minima
- `es_stock_bajo`: cantidad_actual < (cantidad_minima × 0.5)
- `porcentaje_stock`: (cantidad_actual / cantidad_maxima) × 100

### 3. Dashboard Endpoints 📊
- `/stocks/critical`: Monitor inventory in critical condition
- `/alerts/active`: Real-time alert monitoring

### 4. Alert Lifecycle
```
Created (activa)
  ↓
[Option 1] Resolved (resuelta) - sets resolved_at timestamp
[Option 2] Ignored (ignorada) - dismissed without action
```

## DTO Models

### ProcessCreateDTO
```json
{
  "nombre": "string",
  "descripcion": "string | null",
  "tipo_proceso": "produccion|prestamo|almacenamiento|descarte",
  "id_empresa": "uuid"
}
```

### ProductMovementCreateDTO
```json
{
  "codigo_producto": "string",
  "id_proceso_origen": "integer",
  "id_proceso_destino": "integer",
  "cantidad": "float > 0",
  "notas": "string | null",
  "id_empresa": "uuid"
}
```

### ChemicalStockCreateDTO
```json
{
  "codigo_producto": "string",
  "id_proceso": "integer",
  "cantidad_actual": "float ≥ 0",
  "cantidad_minima": "float > 0",
  "cantidad_maxima": "float > 0",
  "unidad_medida": "string",
  "id_empresa": "uuid"
}
```

### StockAlertCreateDTO
```json
{
  "codigo_producto": "string",
  "id_proceso": "integer",
  "tipo_alerta": "stock_critico|stock_bajo|exceso",
  "cantidad_actual": "float ≥ 0",
  "cantidad_referencia": "float ≥ 0",
  "id_empresa": "uuid",
  "descripcion": "string | null"
}
```

## Example Workflow

```bash
# 1. Create a production process
POST /processes/
{
  "nombre": "Production Line A",
  "tipo_proceso": "produccion",
  "id_empresa": "company-uuid"
}
# Response: { "id_proceso": 1, ... }

# 2. Create storage process
POST /processes/
{
  "nombre": "Storage",
  "tipo_proceso": "almacenamiento",
  "id_empresa": "company-uuid"
}
# Response: { "id_proceso": 2, ... }

# 3. Initialize chemical stock
POST /stocks/
{
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "cantidad_actual": 100,
  "cantidad_minima": 50,
  "cantidad_maxima": 200,
  "unidad_medida": "ml",
  "id_empresa": "company-uuid"
}

# 4. Move product to storage (triggers alert if stock < min)
POST /movements/
{
  "codigo_producto": "CHEM001",
  "id_proceso_origen": 1,
  "id_proceso_destino": 2,
  "cantidad": 60,
  "notas": "Transfer to storage",
  "id_empresa": "company-uuid"
}
# System detects: 100 - 60 = 40 < 50 (minimum)
# ⚡ Automatically creates StockAlert with tipo_alerta="stock_critico"

# 5. Check critical stocks
GET /stocks/critical?company_id=company-uuid

# 6. Check active alerts
GET /alerts/active?company_id=company-uuid

# 7. Resolve alert  
PATCH /alerts/1/resolve
# Updates: estado="resuelta", resolved_at=now()
```

## Alert Types

| Type | Trigger | Priority | Example |
|------|---------|----------|---------|
| `stock_critico` | cantidad < min | 🔴 URGENT | 8ml < 50ml minimum |
| `stock_bajo` | 25-50% of min | 🟠 WARNING | 15ml < 25ml warning zone |
| `exceso` | cantidad > max | 🟡 INFO | 220ml > 200ml capacity |

## Common Queries

### Get all movements for a product
```
GET /movements/?company_id=uuid&codigo_producto=CHEM001
```

### Track critical items
```
GET /stocks/critical?company_id=uuid
```

### Monitor system for issues
```
GET /alerts/active?company_id=uuid
```

### Check inventory status
```
GET /stocks/{id}?company_id=uuid
```
Returns properties: `es_stock_critico`, `es_stock_bajo`, `porcentaje_stock`

## Error Responses

```json
{
  "detail": "Error message"
}
```

| Code | Scenario |
|------|----------|
| 400 | Invalid input (min > max, negative quantity, etc) |
| 404 | Entity not found |
| 201 | Created successfully |
| 204 | Deleted successfully |

## Performance Notes

- `/stocks/critical` query uses database filter: `cantidad_actual < cantidad_minima`
- `/alerts/active` query filters: `estado = 'activa'`
- All endpoints accept `company_id` to enforce data isolation
- Automatic alert creation happens during movement POST (transactional)

## Architecture

Following Hexagonal Architecture:
- **Domain**: Business logic (entities, ports)
- **Application**: Use cases (orchestration)
- **Infrastructure**: Data persistence (ORM, HTTP endpoints)

All endpoints use dependency injection for loose coupling and testability.
