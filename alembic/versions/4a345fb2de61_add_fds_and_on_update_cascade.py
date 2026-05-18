"""add fds and on update cascade

Revision ID: 4a345fb2de61
Revises: consolidate_heads
Create Date: 2026-05-18 06:56:22.387338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a345fb2de61'
down_revision: Union[str, Sequence[str], None] = 'consolidate_heads'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # 1. Add fds and fds_url to products if they don't exist
    prod_columns = [c['name'] for c in inspector.get_columns('products')]
    
    if 'fds' not in prod_columns:
        op.add_column('products', sa.Column('fds', sa.String(), nullable=True))
    if 'fds_url' not in prod_columns:
        op.add_column('products', sa.Column('fds_url', sa.String(), nullable=True))
        
    # Helper to check if a foreign key constraint exists
    def has_fk(table, fk_name):
        fks = inspector.get_foreign_keys(table)
        return any(fk['name'] == fk_name for fk in fks)
        
    # Helper to check if any foreign key exists on a specific column
    def get_fk_name_on_col(table, col_name):
        fks = inspector.get_foreign_keys(table)
        for fk in fks:
            if col_name in fk['constrained_columns']:
                return fk['name']
        return None

    # 2. Drop existing foreign keys dynamically
    fk_mappings = [
        ('stock_almacen', 'stock_almacen_codigo_producto_fkey', 'codigo_producto'),
        ('stock_ubicacion', 'stock_ubicacion_codigo_producto_fkey', 'codigo_producto'),
        ('producto_proveedor', 'producto_proveedor_codigo_producto_fkey', 'codigo_producto'),
        ('stock_quimicos', 'stock_quimicos_codigo_producto_fkey', 'codigo_producto'),
        ('movimientos_productos', 'movimientos_productos_codigo_producto_fkey', 'codigo_producto'),
    ]
    
    for table, standard_name, col in fk_mappings:
        # Check standard name first
        if has_fk(table, standard_name):
            op.drop_constraint(standard_name, table, type_='foreignkey')
        else:
            # Check if there is another foreign key on the same column (created under a different system name)
            alternative_name = get_fk_name_on_col(table, col)
            if alternative_name:
                op.drop_constraint(alternative_name, table, type_='foreignkey')
                
    # 3. Recreate foreign keys with onupdate="CASCADE"
    # (Checking if constraint already has the exact name, if so skip or drop it first)
    recreate_fks = [
        ('stock_almacen_codigo_producto_fkey', 'stock_almacen', 'codigo_producto'),
        ('stock_ubicacion_codigo_producto_fkey', 'stock_ubicacion', 'codigo_producto'),
        ('producto_proveedor_codigo_producto_fkey', 'producto_proveedor', 'codigo_producto'),
        ('stock_quimicos_codigo_producto_fkey', 'stock_quimicos', 'codigo_producto'),
        ('movimientos_productos_codigo_producto_fkey', 'movimientos_productos', 'codigo_producto'),
    ]
    
    for name, table, col in recreate_fks:
        if not has_fk(table, name):
            op.create_foreign_key(
                name,
                table, 'products',
                [col], ['id_product'],
                onupdate='CASCADE'
            )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Helper to check if a foreign key constraint exists
    def has_fk(table, fk_name):
        fks = inspector.get_foreign_keys(table)
        return any(fk['name'] == fk_name for fk in fks)

    # 1. Drop the cascading foreign keys
    fks_to_drop = [
        ('stock_almacen_codigo_producto_fkey', 'stock_almacen'),
        ('stock_ubicacion_codigo_producto_fkey', 'stock_ubicacion'),
        ('producto_proveedor_codigo_producto_fkey', 'producto_proveedor'),
        ('stock_quimicos_codigo_producto_fkey', 'stock_quimicos'),
        ('movimientos_productos_codigo_producto_fkey', 'movimientos_productos'),
    ]
    
    for name, table in fks_to_drop:
        if has_fk(table, name):
            op.drop_constraint(name, table, type_='foreignkey')
            
    # 2. Recreate foreign keys without cascade on update
    recreate_fks = [
        ('stock_almacen_codigo_producto_fkey', 'stock_almacen', 'codigo_producto'),
        ('stock_ubicacion_codigo_producto_fkey', 'stock_ubicacion', 'codigo_producto'),
        ('producto_proveedor_codigo_producto_fkey', 'producto_proveedor', 'codigo_producto'),
        ('stock_quimicos_codigo_producto_fkey', 'stock_quimicos', 'codigo_producto'),
        ('movimientos_productos_codigo_producto_fkey', 'movimientos_productos', 'codigo_producto'),
    ]
    
    for name, table, col in recreate_fks:
        if not has_fk(table, name):
            op.create_foreign_key(
                name,
                table, 'products',
                [col], ['id_product']
            )
            
    # 3. Drop columns from products if they exist
    prod_columns = [c['name'] for c in inspector.get_columns('products')]
    if 'fds_url' in prod_columns:
        op.drop_column('products', 'fds_url')
    if 'fds' in prod_columns:
        op.drop_column('products', 'fds')
