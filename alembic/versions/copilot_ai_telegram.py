"""copilot ai and telegram integration

Revision ID: copilot_ai_telegram
Revises: 9c4d2e7a1b6f
Create Date: 2026-06-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


# revision identifiers, used by Alembic.
revision: str = 'copilot_ai_telegram'
down_revision: Union[str, Sequence[str], None] = '9c4d2e7a1b6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create copilot chat, telegram and replenishment tables."""
    op.create_table(
        'copilot_conversations',
        sa.Column('id_conversation', PG_UUID(as_uuid=True), primary_key=True),
        sa.Column('id_empresa', PG_UUID(as_uuid=True), nullable=True),
        sa.Column('id_usuario', PG_UUID(as_uuid=True), nullable=True),
        sa.Column('canal', sa.String(length=20), nullable=False, server_default='web'),
        sa.Column('canal_chat_id', sa.String(length=64), nullable=True),
        sa.Column('alerta_id', sa.Integer(), nullable=True),
        sa.Column('codigo_producto', sa.String(length=50), nullable=True),
        sa.Column('titulo', sa.String(length=200), nullable=True),
        sa.Column('estado', sa.String(length=20), nullable=False, server_default='activa'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['id_empresa'], ['companies.id_company']),
        sa.ForeignKeyConstraint(['id_usuario'], ['users.id_user']),
        sa.ForeignKeyConstraint(['alerta_id'], ['alertas_stock.id_alerta']),
    )

    op.create_table(
        'copilot_messages',
        sa.Column('id_mensaje', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_conversation', PG_UUID(as_uuid=True), nullable=False),
        sa.Column('rol', sa.String(length=20), nullable=False),
        sa.Column('contenido', sa.Text(), nullable=False),
        sa.Column('canal', sa.String(length=20), nullable=True),
        sa.Column('proveedor', sa.String(length=40), nullable=True),
        sa.Column('modelo', sa.String(length=80), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['id_conversation'], ['copilot_conversations.id_conversation'], ondelete='CASCADE'
        ),
    )

    op.create_table(
        'telegram_accounts',
        sa.Column('id_cuenta', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', PG_UUID(as_uuid=True), nullable=False),
        sa.Column('chat_id', sa.BigInteger(), nullable=False),
        sa.Column('telegram_username', sa.String(length=100), nullable=True),
        sa.Column('id_empresa', PG_UUID(as_uuid=True), nullable=True),
        sa.Column('linked_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id_user']),
        sa.ForeignKeyConstraint(['id_empresa'], ['companies.id_company']),
        sa.UniqueConstraint('user_id', name='uq_telegram_accounts_user'),
        sa.UniqueConstraint('chat_id', name='uq_telegram_accounts_chat'),
    )

    op.create_table(
        'telegram_link_codes',
        sa.Column('code', sa.String(length=12), primary_key=True),
        sa.Column('user_id', PG_UUID(as_uuid=True), nullable=False),
        sa.Column('id_empresa', PG_UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id_user']),
        sa.ForeignKeyConstraint(['id_empresa'], ['companies.id_company']),
    )

    op.create_table(
        'telegram_updates',
        sa.Column('update_id', sa.BigInteger(), primary_key=True),
        sa.Column('processed_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'replenishment_drafts',
        sa.Column('id_borrador', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_empresa', PG_UUID(as_uuid=True), nullable=False),
        sa.Column('alerta_id', sa.Integer(), nullable=True),
        sa.Column('id_conversation', PG_UUID(as_uuid=True), nullable=True),
        sa.Column('codigo_producto', sa.String(length=50), nullable=False),
        sa.Column('cantidad_sugerida', sa.Float(), nullable=True),
        sa.Column('unidad_medida', sa.String(length=20), nullable=True),
        sa.Column('proveedor_sugerido', sa.String(length=50), nullable=True),
        sa.Column('notas', sa.String(length=500), nullable=True),
        sa.Column('estado', sa.String(length=30), nullable=False, server_default='pendiente_revision'),
        sa.Column('created_by', PG_UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['id_empresa'], ['companies.id_company']),
        sa.ForeignKeyConstraint(['alerta_id'], ['alertas_stock.id_alerta']),
        sa.ForeignKeyConstraint(
            ['id_conversation'], ['copilot_conversations.id_conversation'], ondelete='SET NULL'
        ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id_user']),
    )

    op.create_index(
        'ix_copilot_conversations_empresa', 'copilot_conversations', ['id_empresa']
    )
    op.create_index(
        'ix_copilot_conversations_canal_chat', 'copilot_conversations', ['canal', 'canal_chat_id']
    )
    op.create_index('ix_copilot_messages_conversation', 'copilot_messages', ['id_conversation'])
    op.create_index('ix_replenishment_drafts_empresa', 'replenishment_drafts', ['id_empresa'])


def downgrade() -> None:
    """Drop copilot tables."""
    op.drop_index('ix_replenishment_drafts_empresa', table_name='replenishment_drafts')
    op.drop_index('ix_copilot_messages_conversation', table_name='copilot_messages')
    op.drop_index('ix_copilot_conversations_canal_chat', table_name='copilot_conversations')
    op.drop_index('ix_copilot_conversations_empresa', table_name='copilot_conversations')
    op.drop_table('replenishment_drafts')
    op.drop_table('telegram_updates')
    op.drop_table('telegram_link_codes')
    op.drop_table('telegram_accounts')
    op.drop_table('copilot_messages')
    op.drop_table('copilot_conversations')
