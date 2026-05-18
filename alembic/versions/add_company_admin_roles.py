"""Add company-scoped admin roles

Revision ID: add_company_admin_roles
Revises: 80ee4920c4d7
Create Date: 2026-04-21

This migration:
1. Creates company_admin roles for existing companies
2. Updates users to have company-scoped admin roles instead of global admin

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid
from uuid import uuid4


revision: str = 'add_company_admin_roles'
down_revision: Union[str, Sequence[str], None] = '80ee4920c4d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add company admin roles."""
    # Get existing companies
    connection = op.get_bind()
    result = connection.execute(sa.text("SELECT id_company, name FROM companies"))
    companies = result.fetchall()
    
    # Get the global admin role ID from settings or use a placeholder
    # You'll need to update this after running or set ADMIN_ROLE_ID in environment
    global_admin_role = None
    
    # Get existing global admin role
    role_result = connection.execute(sa.text("SELECT id_role FROM roles WHERE name = 'Admin'"))
    existing_role = role_result.fetchone()
    if existing_role:
        global_admin_role = existing_role[0]
    
    for company in companies:
        company_id = company[0]
        company_name = company[1]
        
        # Create company_admin role for this company (deterministic UUID)
        company_admin_role_id = uuid.uuid5(uuid.NAMESPACE_OID, f"company_admin_{company_id}")
        
        # Check if role already exists
        check_role = connection.execute(
            sa.text("SELECT id_role FROM roles WHERE id_role = :role_id"),
            {"role_id": company_admin_role_id}
        ).fetchone()
        
        if not check_role:
            connection.execute(
                sa.text("""
                    INSERT INTO roles (id_role, name)
                    VALUES (:role_id, :name)
                """),
                {"role_id": company_admin_role_id, "name": f"Admin - {company_name}"}
            )
        
        # Update users who were previously admin for this company
        # Check if any users have the global admin role and belong to this company
        if global_admin_role:
            connection.execute(
                sa.text("""
                    UPDATE users 
                    SET role_id = :new_role_id
                    WHERE role_id = :old_role_id AND company_id = :company_id
                """),
                {
                    "new_role_id": company_admin_role_id,
                    "old_role_id": global_admin_role,
                    "company_id": company_id
                }
            )


def downgrade() -> None:
    """Remove company admin roles and restore global admin."""
    connection = op.get_bind()
    
    # Get all company_admin roles
    result = connection.execute(
        sa.text("SELECT id_role FROM roles WHERE name LIKE 'Admin - %'")
    )
    company_admin_roles = result.fetchall()
    
    # Get global admin role
    role_result = connection.execute(
        sa.text("SELECT id_role FROM roles WHERE name = 'Admin'")
    )
    global_admin = role_result.fetchone()
    
    if global_admin:
        global_admin_role_id = global_admin[0]
        
        for role in company_admin_roles:
            role_id = role[0]
            
            # Update users back to global admin
            connection.execute(
                sa.text("""
                    UPDATE users
                    SET role_id = :global_role_id
                    WHERE role_id = :company_role_id
                """),
                {
                    "global_role_id": global_admin_role_id,
                    "company_role_id": role_id
                }
            )
            
            # Delete company admin role
            connection.execute(
                sa.text("DELETE FROM roles WHERE id_role = :role_id"),
                {"role_id": role_id}
            )