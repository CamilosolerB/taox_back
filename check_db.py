from app.infrastructure.db.engine import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT id_user, username, email, role_id, company_id FROM users"))
    print('Users:')
    for row in result:
        print(row)
    
    result2 = conn.execute(text("SELECT id_role, name FROM roles"))
    print('\nRoles:')
    for row in result2:
        print(row)
