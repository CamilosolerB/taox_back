import os
from sqlalchemy import create_engine, inspect

db_url = "postgresql+psycopg2://postgres:Camilo123$@localhost:5432/taox"
engine = create_engine(db_url)
inspector = inspect(engine)

tables = ["products", "stock_almacen", "stock_ubicacion", "producto_proveedor", "stock_quimicos", "movimientos_productos"]

for table in tables:
    print(f"\nTable: {table}")
    # Columns
    cols = inspector.get_columns(table)
    print("  Columns:")
    for c in cols:
        print(f"    {c['name']}: {c['type']} (nullable={c['nullable']})")
    
    # Foreign Keys
    fks = inspector.get_foreign_keys(table)
    print("  Foreign Keys:")
    for fk in fks:
        print(f"    Name: {fk['name']}, Constrained: {fk['constrained_columns']}, Referred: {fk['referred_table']} -> {fk['referred_columns']}")
