"""Support global administrators and client legal names.

Revision ID: 9c4d2e7a1b6f
Revises: c33156a66ff2
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9c4d2e7a1b6f"
down_revision: Union[str, Sequence[str], None] = "c33156a66ff2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "company_id",
        existing_type=sa.UUID(),
        existing_nullable=False,
        nullable=True,
    )
    op.alter_column(
        "stock_almacen",
        "cantidad",
        existing_type=sa.Integer(),
        existing_nullable=False,
        type_=sa.Float(),
        postgresql_using="cantidad::double precision",
    )
    op.alter_column(
        "stock_ubicacion",
        "cantidad",
        existing_type=sa.Integer(),
        existing_nullable=False,
        type_=sa.Float(),
        postgresql_using="cantidad::double precision",
    )
    op.add_column(
        "cliente",
        sa.Column("razon_social", sa.String(length=100), nullable=True),
    )


def downgrade() -> None:
    connection = op.get_bind()
    fractional_stock = connection.execute(
        sa.text(
            "SELECT EXISTS ("
            "SELECT 1 FROM stock_almacen WHERE cantidad <> trunc(cantidad) "
            "UNION ALL "
            "SELECT 1 FROM stock_ubicacion WHERE cantidad <> trunc(cantidad)"
            ")"
        )
    ).scalar()
    if fractional_stock:
        raise RuntimeError(
            "Cannot downgrade stock quantities to integers while fractional "
            "quantities exist."
        )
    global_admin_without_company = connection.execute(
        sa.text("SELECT EXISTS (SELECT 1 FROM users WHERE company_id IS NULL)")
    ).scalar()
    if global_admin_without_company:
        raise RuntimeError(
            "Cannot downgrade while global administrator accounts without a "
            "company exist."
        )
    op.drop_column("cliente", "razon_social")
    op.alter_column(
        "stock_almacen",
        "cantidad",
        existing_type=sa.Float(),
        existing_nullable=False,
        type_=sa.Integer(),
        postgresql_using="cantidad::integer",
    )
    op.alter_column(
        "stock_ubicacion",
        "cantidad",
        existing_type=sa.Float(),
        existing_nullable=False,
        type_=sa.Integer(),
        postgresql_using="cantidad::integer",
    )
    op.alter_column(
        "users",
        "company_id",
        existing_type=sa.UUID(),
        existing_nullable=True,
        nullable=False,
    )
