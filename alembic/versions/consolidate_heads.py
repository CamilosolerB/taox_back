"""Consolidate all heads - warehouse + company roles

Revision ID: consolidate_heads
Revises: 4b3f454a5135, add_warehouse_id_products
Create Date: 2026-04-21

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'consolidate_heads'
down_revision: Union[str, Sequence[str], None] = ('4b3f454a5135', 'add_company_admin_roles')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add warehouse_id to products table."""
    # Check if column already exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('products')]
    
    if 'warehouse_id' not in columns:
        # Add warehouse_id column to products
        op.add_column('products', 
            sa.Column('warehouse_id', sa.UUID(), nullable=True)
        )
        
        # Add foreign key constraint
        op.create_foreign_key(
            'fk_products_warehouse',
            'products', 'procesos',
            ['warehouse_id'], ['id_proceso']
        )


def downgrade() -> None:
    """Remove warehouse_id."""
    op.drop_constraint('fk_products_warehouse', 'products', type_='foreignkey')
    op.drop_column('products', 'warehouse_id')