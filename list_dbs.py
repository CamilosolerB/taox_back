from sqlalchemy import create_engine, text

db_url = "postgresql+psycopg2://postgres:Camilo123$@localhost:5432/postgres"
engine = create_engine(db_url)

with engine.connect() as conn:
    res = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
    print("Databases in Postgres:")
    for row in res:
        print(f"  {row[0]}")
