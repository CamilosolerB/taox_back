# Arquitectura propuesta

```bash
project/
│
├── app/
│   ├── api/                    # Interface layer
│   │   ├── routes/
│   │   │   └── users.py
│   │   └── dependencies/
│   │       └── db.py
│   │
│   ├── core/                   # Config global
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── domain/                 # Entidades y interfaces abstractas
│   │   ├── models/
│   │   │   └── user.py
│   │   └── repositories/
│   │       └── user_repository.py
│   │
│   ├── infrastructure/         # Implementaciones concretas
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── entities.py     # SQLAlchemy tables
│   │   └── repositories/
│   │       └── user_dao.py     # DAO
│   │
│   ├── services/               # Application / Use cases
│   │   └── user_service.py
│   │
│   ├── schemas/                # Pydantic request/response
│   │   └── user_schema.py
│   │
│   └── main.py                 # Punto de entrada FastAPI
│
├── tests/
│   └── ...
│
├── requirements.txt
└── README.md

```

## run FasAPI

```bash
python -m uvicorn app.main:app --reload
```

## Alembic migrations

### Autogenerate (validar)

```bash
alembic revision --autogenerate -m "create users table"
```

### Migrar

```bash
alembic upgrade head
```
