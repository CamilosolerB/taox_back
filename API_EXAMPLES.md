# API REQUEST/RESPONSE EXAMPLES

## Processes

### Create Process
**Request:**
```bash
POST /processes/
```

**Body:**
```json
{
  "nombre": "Production Line A",
  "descripcion": "Main chemical production facility",
  "tipo_proceso": "produccion",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (201 Created):**
```json
{
  "id_proceso": 1,
  "nombre": "Production Line A",
  "descripcion": "Main chemical production facility",
  "tipo_proceso": "produccion",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true,
  "created_at": "2025-03-01T10:00:00",
  "updated_at": "2025-03-01T10:00:00"
}
```

### List Processes
**Request:**
```bash
GET /processes/?company_id=550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
[
  {
    "id_proceso": 1,
    "nombre": "Production Line A",
    "descripcion": "Main chemical production facility",
    "tipo_proceso": "produccion",
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
    "is_active": true,
    "created_at": "2025-03-01T10:00:00",
    "updated_at": "2025-03-01T10:00:00"
  },
  {
    "id_proceso": 2,
    "nombre": "Storage Warehouse B",
    "descripcion": "Primary storage facility",
    "tipo_proceso": "almacenamiento",
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
    "is_active": true,
    "created_at": "2025-03-01T10:05:00",
    "updated_at": "2025-03-01T10:05:00"
  }
]
```

### Update Process
**Request:**
```bash
PUT /processes/1
```

**Body:**
```json
{
  "nombre": "Production Line A - Updated",
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "id_proceso": 1,
  "nombre": "Production Line A - Updated",
  "descripcion": "Main chemical production facility",
  "tipo_proceso": "produccion",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true,
  "created_at": "2025-03-01T10:00:00",
  "updated_at": "2025-03-01T10:15:00"
}
```

---

## Product Movements

### Create Movement
**Request:**
```bash
POST /movements/
```

**Body:**
```json
{
  "codigo_producto": "CHEM001",
  "id_proceso_origen": 1,
  "id_proceso_destino": 2,
  "cantidad": 60.5,
  "notas": "Transfer from production to storage",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (201 Created):**
```json
{
  "id_movimiento": 1,
  "codigo_producto": "CHEM001",
  "id_proceso_origen": 1,
  "id_proceso_destino": 2,
  "cantidad": 60.5,
  "notas": "Transfer from production to storage",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "estado": "pendiente",
  "created_at": "2025-03-01T10:30:00",
  "updated_at": "2025-03-01T10:30:00"
}
```

**Side Effect:** If destination stock falls below minimum, an alert is automatically created:
```json
{
  "id_alerta": 1,
  "codigo_producto": "CHEM001",
  "id_proceso": 2,
  "tipo_alerta": "stock_critico",
  "cantidad_actual": 40.0,
  "cantidad_referencia": 50.0,
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "estado": "activa",
  "descripcion": "Stock critical: 40.0 < 50.0 minimum",
  "resolved_at": null,
  "created_at": "2025-03-01T10:30:00",
  "updated_at": "2025-03-01T10:30:00"
}
```

### Update Movement Status
**Request:**
```bash
PATCH /movements/1/status?nuevo_estado=completado
```

**Response (200 OK):**
```json
{
  "id_movimiento": 1,
  "codigo_producto": "CHEM001",
  "id_proceso_origen": 1,
  "id_proceso_destino": 2,
  "cantidad": 60.5,
  "notas": "Transfer from production to storage",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "estado": "completado",
  "created_at": "2025-03-01T10:30:00",
  "updated_at": "2025-03-01T10:35:00"
}
```

---

## Chemical Stocks

### Create Stock
**Request:**
```bash
POST /stocks/
```

**Body:**
```json
{
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "cantidad_actual": 100.0,
  "cantidad_minima": 50.0,
  "cantidad_maxima": 200.0,
  "unidad_medida": "ml",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (201 Created):**
```json
{
  "id_stock_quimico": 1,
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "cantidad_actual": 100.0,
  "cantidad_minima": 50.0,
  "cantidad_maxima": 200.0,
  "unidad_medida": "ml",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true,
  "es_stock_critico": false,
  "es_stock_bajo": false,
  "porcentaje_stock": 50.0,
  "created_at": "2025-03-01T10:20:00",
  "updated_at": "2025-03-01T10:20:00"
}
```

### Get Critical Stocks (Dashboard)
**Request:**
```bash
GET /stocks/critical?company_id=550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
[
  {
    "id_stock_quimico": 2,
    "codigo_producto": "CHEM001",
    "id_proceso": 2,
    "cantidad_actual": 40.0,
    "cantidad_minima": 50.0,
    "cantidad_maxima": 200.0,
    "unidad_medida": "ml",
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
    "is_active": true,
    "es_stock_critico": true,
    "es_stock_bajo": false,
    "porcentaje_stock": 20.0,
    "created_at": "2025-03-01T10:20:00",
    "updated_at": "2025-03-01T10:30:00"
  },
  {
    "id_stock_quimico": 3,
    "codigo_producto": "CHEM002",
    "id_proceso": 1,
    "cantidad_actual": 5.0,
    "cantidad_minima": 20.0,
    "cantidad_maxima": 100.0,
    "unidad_medida": "g",
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
    "is_active": true,
    "es_stock_critico": true,
    "es_stock_bajo": false,
    "porcentaje_stock": 5.0,
    "created_at": "2025-03-01T09:00:00",
    "updated_at": "2025-03-01T09:45:00"
  }
]
```

### Get Stock by ID
**Request:**
```bash
GET /stocks/1?company_id=550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "id_stock_quimico": 1,
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "cantidad_actual": 100.0,
  "cantidad_minima": 50.0,
  "cantidad_maxima": 200.0,
  "unidad_medida": "ml",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true,
  "es_stock_critico": false,
  "es_stock_bajo": false,
  "porcentaje_stock": 50.0,
  "created_at": "2025-03-01T10:20:00",
  "updated_at": "2025-03-01T10:20:00"
}
```

### Update Stock
**Request:**
```bash
PUT /stocks/1
```

**Body:**
```json
{
  "cantidad_actual": 120.0,
  "cantidad_minima": 45.0
}
```

**Response (200 OK):**
```json
{
  "id_stock_quimico": 1,
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "cantidad_actual": 120.0,
  "cantidad_minima": 45.0,
  "cantidad_maxima": 200.0,
  "unidad_medida": "ml",
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true,
  "es_stock_critico": false,
  "es_stock_bajo": false,
  "porcentaje_stock": 60.0,
  "created_at": "2025-03-01T10:20:00",
  "updated_at": "2025-03-01T10:40:00"
}
```

---

## Stock Alerts

### Create Alert (Manual)
**Request:**
```bash
POST /alerts/
```

**Body:**
```json
{
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "tipo_alerta": "stock_bajo",
  "cantidad_actual": 30.0,
  "cantidad_referencia": 50.0,
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "descripcion": "Inventory approaching minimum level"
}
```

**Response (201 Created):**
```json
{
  "id_alerta": 2,
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "tipo_alerta": "stock_bajo",
  "cantidad_actual": 30.0,
  "cantidad_referencia": 50.0,
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "estado": "activa",
  "descripcion": "Inventory approaching minimum level",
  "resolved_at": null,
  "created_at": "2025-03-01T11:00:00",
  "updated_at": "2025-03-01T11:00:00"
}
```

### Get Active Alerts (Dashboard)
**Request:**
```bash
GET /alerts/active?company_id=550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
[
  {
    "id_alerta": 1,
    "codigo_producto": "CHEM001",
    "id_proceso": 2,
    "tipo_alerta": "stock_critico",
    "cantidad_actual": 40.0,
    "cantidad_referencia": 50.0,
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
    "estado": "activa",
    "descripcion": "Critical level reached: 40.0ml < 50ml minimum",
    "resolved_at": null,
    "created_at": "2025-03-01T10:30:00",
    "updated_at": "2025-03-01T10:30:00"
  },
  {
    "id_alerta": 2,
    "codigo_producto": "CHEM001",
    "id_proceso": 1,
    "tipo_alerta": "stock_bajo",
    "cantidad_actual": 30.0,
    "cantidad_referencia": 50.0,
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
    "estado": "activa",
    "descripcion": "Inventory approaching minimum level",
    "resolved_at": null,
    "created_at": "2025-03-01T11:00:00",
    "updated_at": "2025-03-01T11:00:00"
  }
]
```

### Resolve Alert
**Request:**
```bash
PATCH /alerts/1/resolve
```

**Response (200 OK):**
```json
{
  "id_alerta": 1,
  "codigo_producto": "CHEM001",
  "id_proceso": 2,
  "tipo_alerta": "stock_critico",
  "cantidad_actual": 40.0,
  "cantidad_referencia": 50.0,
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "estado": "resuelta",
  "descripcion": "Critical level reached: 40.0ml < 50ml minimum",
  "resolved_at": "2025-03-01T11:30:00",
  "created_at": "2025-03-01T10:30:00",
  "updated_at": "2025-03-01T11:30:00"
}
```

### Update Alert Status
**Request:**
```bash
PUT /alerts/2
```

**Body:**
```json
{
  "estado": "ignorada",
  "descripcion": "Dismissed - restock planned for tomorrow"
}
```

**Response (200 OK):**
```json
{
  "id_alerta": 2,
  "codigo_producto": "CHEM001",
  "id_proceso": 1,
  "tipo_alerta": "stock_bajo",
  "cantidad_actual": 30.0,
  "cantidad_referencia": 50.0,
  "id_empresa": "550e8400-e29b-41d4-a716-446655440000",
  "estado": "ignorada",
  "descripcion": "Dismissed - restock planned for tomorrow",
  "resolved_at": null,
  "created_at": "2025-03-01T11:00:00",
  "updated_at": "2025-03-01T11:35:00"
}
```

---

## Error Responses

### Bad Request (400)
```json
{
  "detail": "cantidad_minima no puede ser mayor a cantidad_maxima"
}
```

### Not Found (404)
```json
{
  "detail": "Process with ID 99 does not exist"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "cantidad"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## Curl Examples

### Create Process
```bash
curl -X POST "http://localhost:8000/processes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Production Line A",
    "tipo_proceso": "produccion",
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### List Critical Stocks
```bash
curl -X GET "http://localhost:8000/stocks/critical?company_id=550e8400-e29b-41d4-a716-446655440000"
```

### Create Movement
```bash
curl -X POST "http://localhost:8000/movements/" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_producto": "CHEM001",
    "id_proceso_origen": 1,
    "id_proceso_destino": 2,
    "cantidad": 60.5,
    "id_empresa": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### Get Active Alerts
```bash
curl -X GET "http://localhost:8000/alerts/active?company_id=550e8400-e29b-41d4-a716-446655440000"
```

### Resolve Alert
```bash
curl -X PATCH "http://localhost:8000/alerts/1/resolve"
```

---

## Http Only (no auth required)

All endpoints are currently accessible without JWT authentication. 
To add authentication, add JWT dependencies to endpoint functions.
