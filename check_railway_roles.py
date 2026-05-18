import sys
from sqlalchemy import create_engine, text

db_url = "postgresql+psycopg2://postgres:QJAFttLWJcuLpQEzpxeufSqmVfcyhZWa@mainline.proxy.rlwy.net:45575/railway"

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("--- CONEXIÓN EXITOSA ---")
        
        # 1. Ver roles
        roles = conn.execute(text("SELECT id_role, name FROM roles")).fetchall()
        print("Roles existentes:")
        for r in roles:
            print(f"  - {r[0]}: {r[1]}")
            
        # 2. Ver empresas
        companies = conn.execute(text("SELECT id_company, name FROM companies")).fetchall()
        print("\nEmpresas existentes:")
        for c in companies:
            print(f"  - {c[0]}: {c[1]}")
            
except Exception as e:
    print("Error al conectar o consultar:", e)
    sys.exit(1)
