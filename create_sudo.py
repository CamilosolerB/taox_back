import sys
import os

# Ensure app is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models.user_orm import User
from app.infrastructure.db.models.role_orm import Role
from app.core.security import hash_password
from app.settings import settings

def main():
    db = SessionLocal()
    try:
        # Check if ADMIN_ROLE_ID exists in roles table
        admin_role = db.query(Role).filter(Role.id_role == settings.ADMIN_ROLE_ID).first()
        if not admin_role:
            print("Creating Admin role...")
            admin_role = Role(id_role=settings.ADMIN_ROLE_ID, name="SuperAdmin")
            db.add(admin_role)
            db.commit()
            print("Admin role created.")

        admin_email = "admin@taox.com"
        existing_user = db.query(User).filter(User.email == admin_email).first()
        
        if existing_user:
            print(f"Sudo user '{admin_email}' already exists!")
            if existing_user.company_id is not None:
                existing_user.company_id = None
                print("Removed company_id from existing Sudo user.")
            db.commit()
        else:
            print(f"Creating Sudo user '{admin_email}'...")
            new_user = User(
                username="Sudo Admin",
                email=admin_email,
                password=hash_password("SudoAdmin2026!"),
                is_active=True,
                role_id=settings.ADMIN_ROLE_ID,
                company_id=None
            )
            db.add(new_user)
            db.commit()
            print("Sudo user successfully created.")

    except Exception as e:
        db.rollback()
        print(f"Error creating Sudo user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
