from app.infrastructure.db.engine import engine
from sqlalchemy import text
from app.core.security import verify_password

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT id_user, username, email, password, role_id, is_active 
        FROM users WHERE email = 'test@example.com'
    """))
    row = result.fetchone()
    if row:
        print(f"User: {row.username}")
        
        # Test password
        test_password = "Mypassw0rd@2024"
        is_valid = verify_password(test_password, row.password)
        print(f"Password '{test_password}' valid: {is_valid}")
        
        if is_valid:
            print("\n✓ Login should work now!")
        else:
            # Maybe password was created with different settings - let's reset it
            from app.core.security import hash_password
            new_hash = hash_password(test_password)
            conn.execute(text("""
                UPDATE users SET password = :new_hash 
                WHERE email = 'test@example.com'
            """), {"new_hash": new_hash})
            conn.commit()
            print("Password updated in DB")