# SYSTEM ARCHITECTURE DIAGRAMS

## Entity Relationship Diagram

```mermaid
erDiagram
    COMPANY ||--o{ PROCESS : owns
    COMPANY ||--o{ PRODUCT_MOVEMENT : owns
    COMPANY ||--o{ CHEMICAL_STOCK : owns
    COMPANY ||--o{ STOCK_ALERT : owns
    
    PRODUCT ||--o{ PRODUCT_MOVEMENT : involves
    PRODUCT ||--o{ CHEMICAL_STOCK : tracks
    PRODUCT ||--o{ STOCK_ALERT : alerts
    
    PROCESS ||--o{ PRODUCT_MOVEMENT : origin
    PROCESS ||--o{ PRODUCT_MOVEMENT : destination
    PROCESS ||--o{ CHEMICAL_STOCK : stores
    PROCESS ||--o{ STOCK_ALERT : monitors
    
    CHEMICAL_STOCK ||--o{ STOCK_ALERT : generates
    
    COMPANY {
        uuid id_company PK
        string name
        string nit
        boolean is_active
    }
    
    PROCESS {
        int id_proceso PK
        string nombre
        string descripcion
        string tipo_proceso
        uuid id_empresa FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    PRODUCT {
        string id_product PK
        string name
        string unit_measure
        float unit_price
        uuid company_id FK
    }
    
    PRODUCT_MOVEMENT {
        int id_movimiento PK
        string codigo_producto FK
        int id_proceso_origen FK
        int id_proceso_destino FK
        float cantidad
        string notas
        uuid id_empresa FK
        string estado
        datetime created_at
        datetime updated_at
    }
    
    CHEMICAL_STOCK {
        int id_stock_quimico PK
        string codigo_producto FK
        int id_proceso FK
        float cantidad_actual
        float cantidad_minima
        float cantidad_maxima
        string unidad_medida
        uuid id_empresa FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    STOCK_ALERT {
        int id_alerta PK
        string codigo_producto FK
        int id_proceso FK
        int id_stock_quimico FK
        string tipo_alerta
        float cantidad_actual
        float cantidad_referencia
        uuid id_empresa FK
        string estado
        string descripcion
        datetime resolved_at
        datetime created_at
        datetime updated_at
    }
```

## Hexagonal Architecture Layers

```mermaid
graph TB
    subgraph HTTP["HTTP Interface"]
        EP[("FastAPI Endpoints")]
    end
    
    subgraph APP["Application Layer"]
        UC1["GetAllProcessesUseCase"]
        UC2["CreateMovementUseCase"]
        UC3["GetCriticalStocksUseCase"]
        UC4["ResolveAlertUseCase"]
        UC5["...other use cases"]
    end
    
    subgraph DOMAIN["Domain Layer"]
        E1["Process Entity"]
        E2["ProductMovement Entity"]
        E3["ChemicalStock Entity"]
        E4["StockAlert Entity"]
        PORT["Port Interfaces<br/>ProcessRepository<br/>MovementRepository<br/>..."]
    end
    
    subgraph INFRA["Infrastructure Layer"]
        DB[("PostgreSQL Database")]
        ORM["ORM Models<br/>ProcessORM<br/>MovementORM<br/>..."]
        REPO["Repository Implementations<br/>ProcessORMRepository<br/>..."]
    end
    
    EP -->|depends| UC1
    EP -->|depends| UC2
    EP -->|depends| UC3
    EP -->|depends| UC4
    
    UC1 -->|uses| E1
    UC2 -->|uses| E2
    UC2 -->|uses| E3
    UC2 -->|uses| E4
    UC3 -->|uses| E3
    UC4 -->|uses| E4
    
    UC1 -->|calls| PORT
    UC2 -->|calls| PORT
    UC3 -->|calls| PORT
    UC4 -->|calls| PORT
    
    PORT -->|implemented by| REPO
    REPO -->|uses| ORM
    ORM -->|maps to| DB
    
    style HTTP fill:#e1f5ff
    style APP fill:#f3e5f5
    style DOMAIN fill:#fff3e0
    style INFRA fill:#e8f5e9
```

## ProductMovement with Alert Generation Flow

```mermaid
sequenceDiagram
    actor Client as API Client
    participant API as FastAPI Endpoint
    participant UC as CreateMovementUseCase
    participant MRepo as MovementRepository
    participant SRepo as StockRepository
    participant ARepo as AlertRepository
    participant DB as PostgreSQL
    
    Client->>API: POST /movements/
    API->>UC: execute(movement_dto)
    
    UC->>MRepo: create_movement(movement)
    MRepo->>DB: INSERT movimientos_productos
    DB->>MRepo: id_movimiento
    MRepo->>UC: Return created movement
    
    UC->>SRepo: get_stock_by_product_and_process()
    SRepo->>DB: SELECT FROM stock_quimicos WHERE...
    DB->>SRepo: ChemicalStock entity
    SRepo->>UC: Return stock
    
    UC->>UC: Check: es_stock_critico?
    alt Stock is Critical
        UC->>ARepo: create_alert(stock_alert)
        ARepo->>DB: INSERT alertas_stock
        DB->>ARepo: id_alerta
        ARepo->>UC: Alert created
    else Stock is Low
        UC->>ARepo: create_alert(stock_alert)
        ARepo->>DB: INSERT alertas_stock
        DB->>ARepo: id_alerta
        ARepo->>UC: Alert created
    else Stock Normal
        UC->>UC: No alert needed
    end
    
    UC->>API: Return ProductMovement
    API->>Client: 201 Created + response
```

## Alert Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> ACTIVA: create_alert()
    
    ACTIVA --> RESUELTA: PATCH /alerts/{id}/resolve
    ACTIVA --> IGNORADA: PUT /alerts/{id} with estado='ignorada'
    
    RESUELTA --> [*]: lifecycle end
    IGNORADA --> [*]: lifecycle end
    
    note right of ACTIVA
        Alert requires action
        resolved_at = NULL
    end note
    
    note right of RESUELTA
        Alert addressed
        resolved_at = TIMESTAMP
    end note
    
    note right of IGNORADA
        Alert dismissed
        No timestamp set
    end note
```

## Stock Status Computation

```mermaid
graph TD
    A["ChemicalStock Entity<br/>cantidad_actual = 40<br/>cantidad_minima = 50<br/>cantidad_maxima = 200"] 
    
    A --> B{Check<br/>cantidad_actual<br/>< cantidad_minima?}
    B -->|YES| C["es_stock_critico = TRUE<br/>⚠️ CRITICAL"]
    B -->|NO| D{Check<br/>cantidad_actual<br/>< minima × 0.5?}
    D -->|YES| E["es_stock_bajo = TRUE<br/>⚠️ LOW"]
    D -->|NO| F["es_stock_bajo = FALSE<br/>✅ NORMAL"]
    
    A --> G["porcentaje_stock =<br/>cantidad_actual / cantidad_maxima × 100<br/>= 40 / 200 × 100 = 20%"]
    
    C --> H["All computed in domain entity<br/>No separate service needed"]
    E --> H
    F --> H
    G --> H
    
    style C fill:#ffcccc
    style E fill:#ffffcc
    style F fill:#ccffcc
    style H fill:#e1f5ff
```

## API Request Flow

```mermaid
graph LR
    Client["Client"]
    
    Client -->|HTTP Request| Router["FastAPI Router<br/>e.g., /processes/"]
    
    Router -->|Depends| Deps["Dependency Injection<br/>get_get_process_use_case"]
    
    Deps -->|Creates| UseCase["Use Case Instance<br/>GetProcessByIdUseCase"]
    
    UseCase -->|Calls| Entity["Domain Entity<br/>business logic"]
    
    UseCase -->|Calls| Port["Port Interface<br/>ProcessRepository.get_process_by_id"]
    
    Port -->|Implemented by| Repo["Repository Implementation<br/>ProcessORMRepository"]
    
    Repo -->|Uses| ORM["ORM Model<br/>ProcessORM"]
    
    ORM -->|Queries| DB["PostgreSQL Database"]
    
    DB -->|Returns rows| ORM
    ORM -->|Converts| Entity
    Entity -->|Returns to| UseCase
    UseCase -->|Returns to| Router
    Router -->|HTTP Response| Client["Client<br/>JSON Response"]
    
    style Client fill:#fff9c4
    style Router fill:#e1f5ff
    style Deps fill:#f3e5f5
    style UseCase fill:#f3e5f5
    style Entity fill:#fff3e0
    style Port fill:#fff3e0
    style Repo fill:#e8f5e9
    style ORM fill:#e8f5e9
    style DB fill:#e8f5e9
```

## Multi-Tenant Data Isolation

```mermaid
graph TB
    subgraph Company1["Company A (id=uuid-1)"]
        P1["Process 1"]
        P2["Process 2"]
        S1["Stock A"]
        A1["Alert X"]
    end
    
    subgraph Company2["Company B (id=uuid-2)"]
        P3["Process 3"]
        P4["Process 4"]
        S2["Stock B"]
        A2["Alert Y"]
    end
    
    API["API Endpoint<br/>GET /stocks/?<br/>company_id=uuid-1"]
    
    API -->|Filters| WHERE["WHERE id_empresa = uuid-1"]
    WHERE -->|Returns| P1
    WHERE -->|Returns| P2
    WHERE -->|Returns| S1
    WHERE -->|Returns| A1
    
    API -->|Ignores| Company2
    
    style Company1 fill:#c8e6c9
    style Company2 fill:#ffccbc
    style API fill:#e1f5ff
    style WHERE fill:#fff3e0
```

## Database Schema Structure

```
procesos (processes)
├── id_proceso (PK)
├── nombre
├── tipo_proceso (ENUM: produccion, prestamo, almacenamiento, descarte)
└── id_empresa (FK → companies)

movimientos_productos (product movements)
├── id_movimiento (PK)
├── codigo_producto (FK → products)
├── id_proceso_origen (FK → procesos)
├── id_proceso_destino (FK → procesos)
├── estado (ENUM: pendiente, en_transito, completado, cancelado)
└── id_empresa (FK → companies)

stock_quimicos (chemical stocks)
├── id_stock_quimico (PK)
├── codigo_producto (FK → products)
├── id_proceso (FK → procesos)
├── cantidad_actual, cantidad_minima, cantidad_maxima
└── id_empresa (FK → companies)

alertas_stock (stock alerts)
├── id_alerta (PK)
├── codigo_producto (FK → products)
├── id_proceso (FK → procesos)
├── id_stock_quimico (FK → stock_quimicos)
├── tipo_alerta (ENUM: stock_critico, stock_bajo, exceso)
├── estado (ENUM: activa, resuelta, ignorada)
├── resolved_at (NULLABLE timestamp)
└── id_empresa (FK → companies)
```
