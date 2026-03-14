"""change_process_id_to_uuid

Revision ID: 0ee3ceb44209
Revises: 0d2617e2e2a4
Create Date: 2026-03-11 08:20:30.914926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ee3ceb44209'
down_revision: Union[str, Sequence[str], None] = '0d2617e2e2a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - convert id_proceso from INT to UUID."""
    # Clear any existing data in dependent tables
    op.execute("TRUNCATE TABLE alertas_stock CASCADE")
    op.execute("TRUNCATE TABLE stock_quimicos CASCADE")
    op.execute("TRUNCATE TABLE movimientos_productos CASCADE")
    
    # Drop foreign key constraints FIRST
    op.execute("ALTER TABLE stock_quimicos DROP CONSTRAINT IF EXISTS stock_quimicos_id_proceso_fkey CASCADE")
    op.execute("ALTER TABLE alertas_stock DROP CONSTRAINT IF EXISTS alertas_stock_id_proceso_fkey CASCADE")
    op.execute("ALTER TABLE movimientos_productos DROP CONSTRAINT IF EXISTS movimientos_productos_id_proceso_origen_fkey CASCADE")
    op.execute("ALTER TABLE movimientos_productos DROP CONSTRAINT IF EXISTS movimientos_productos_id_proceso_destino_fkey CASCADE")
    
    # Now drop primary key with CASCADE
    op.execute("ALTER TABLE procesos DROP CONSTRAINT procesos_pkey CASCADE")
    
    # Drop sequence
    op.execute("DROP SEQUENCE IF EXISTS procesos_id_proceso_seq CASCADE")
    
    # Change column types to UUID
    op.execute("ALTER TABLE procesos ALTER COLUMN id_proceso TYPE uuid USING gen_random_uuid()")
    op.execute("ALTER TABLE stock_quimicos ALTER COLUMN id_proceso TYPE uuid USING NULL")
    op.execute("ALTER TABLE alertas_stock ALTER COLUMN id_proceso TYPE uuid USING NULL")
    op.execute("ALTER TABLE movimientos_productos ALTER COLUMN id_proceso_origen TYPE uuid USING NULL")
    op.execute("ALTER TABLE movimientos_productos ALTER COLUMN id_proceso_destino TYPE uuid USING NULL")
    
    # Re-add primary key
    op.execute("ALTER TABLE procesos ADD CONSTRAINT procesos_pkey PRIMARY KEY (id_proceso)")
    
    # Re-add foreign keys
    op.execute("ALTER TABLE stock_quimicos ADD CONSTRAINT stock_quimicos_id_proceso_fkey FOREIGN KEY (id_proceso) REFERENCES procesos (id_proceso)")
    op.execute("ALTER TABLE alertas_stock ADD CONSTRAINT alertas_stock_id_proceso_fkey FOREIGN KEY (id_proceso) REFERENCES procesos (id_proceso)")
    op.execute("ALTER TABLE movimientos_productos ADD CONSTRAINT movimientos_productos_id_proceso_origen_fkey FOREIGN KEY (id_proceso_origen) REFERENCES procesos (id_proceso)")
    op.execute("ALTER TABLE movimientos_productos ADD CONSTRAINT movimientos_productos_id_proceso_destino_fkey FOREIGN KEY (id_proceso_destino) REFERENCES procesos (id_proceso)")


def downgrade() -> None:
    """Downgrade schema - revert id_proceso back to INTEGER."""
    # Drop constraints
    op.execute("ALTER TABLE stock_quimicos DROP CONSTRAINT IF EXISTS stock_quimicos_id_proceso_fkey CASCADE")
    op.execute("ALTER TABLE alertas_stock DROP CONSTRAINT IF EXISTS alertas_stock_id_proceso_fkey CASCADE")
    op.execute("ALTER TABLE movimientos_productos DROP CONSTRAINT IF EXISTS movimientos_productos_id_proceso_origen_fkey CASCADE")
    op.execute("ALTER TABLE movimientos_productos DROP CONSTRAINT IF EXISTS movimientos_productos_id_proceso_destino_fkey CASCADE")
    
    # Drop primary key
    op.execute("ALTER TABLE procesos DROP CONSTRAINT procesos_pkey CASCADE")
    
    # Create sequence
    op.execute("CREATE SEQUENCE procesos_id_proceso_seq START WITH 1")
    
    # Revert column types to INTEGER
    op.execute("ALTER TABLE procesos ALTER COLUMN id_proceso TYPE integer USING 1")
    op.execute("ALTER TABLE stock_quimicos ALTER COLUMN id_proceso TYPE integer USING NULL")
    op.execute("ALTER TABLE alertas_stock ALTER COLUMN id_proceso TYPE integer USING NULL")
    op.execute("ALTER TABLE movimientos_productos ALTER COLUMN id_proceso_origen TYPE integer USING NULL")
    op.execute("ALTER TABLE movimientos_productos ALTER COLUMN id_proceso_destino TYPE integer USING NULL")
    
    # Re-add primary key and sequence
    op.execute("ALTER TABLE procesos ADD CONSTRAINT procesos_pkey PRIMARY KEY (id_proceso)")
    op.execute("ALTER SEQUENCE procesos_id_proceso_seq OWNED BY procesos.id_proceso")
    
    # Re-add foreign keys
    op.execute("ALTER TABLE stock_quimicos ADD CONSTRAINT stock_quimicos_id_proceso_fkey FOREIGN KEY (id_proceso) REFERENCES procesos (id_proceso)")
    op.execute("ALTER TABLE alertas_stock ADD CONSTRAINT alertas_stock_id_proceso_fkey FOREIGN KEY (id_proceso) REFERENCES procesos (id_proceso)")
    op.execute("ALTER TABLE movimientos_productos ADD CONSTRAINT movimientos_productos_id_proceso_origen_fkey FOREIGN KEY (id_proceso_origen) REFERENCES procesos (id_proceso)")
    op.execute("ALTER TABLE movimientos_productos ADD CONSTRAINT movimientos_productos_id_proceso_destino_fkey FOREIGN KEY (id_proceso_destino) REFERENCES procesos (id_proceso)")
