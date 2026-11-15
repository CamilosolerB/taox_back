"""Hash any plaintext passwords still stored in users.password.

Revision ID: hash_plaintext_passwords
Revises: copilot_ai_telegram

Some accounts were inserted with plaintext passwords (instead of bcrypt),
which makes login impossible because ``verify_password`` expects a bcrypt hash.
This migration detects any password that is not already a bcrypt hash and
replaces it with the bcrypt hash of the same value, preserving the ability to
log in with the original password.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext


revision: str = "hash_plaintext_passwords"
down_revision: Union[str, Sequence[str], None] = "copilot_ai_telegram"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    connection = op.get_bind()
    rows = connection.execute(
        sa.text(
            "SELECT id_user, password FROM users "
            "WHERE password IS NOT NULL AND password NOT LIKE '$2%'"
        )
    ).fetchall()
    for id_user, password in rows:
        hashed = pwd_context.hash(password[:72])
        connection.execute(
            sa.text("UPDATE users SET password = :password WHERE id_user = :id_user"),
            {"password": hashed, "id_user": id_user},
        )


def downgrade() -> None:
    # Irreversible: the original plaintext values are not recoverable.
    pass
