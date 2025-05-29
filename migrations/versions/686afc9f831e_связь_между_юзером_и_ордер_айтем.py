"""связь между юзером и ордер айтем

Revision ID: 686afc9f831e
Revises: 1ca3924de304
Create Date: 2025-05-29 19:42:38.235187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '686afc9f831e'
down_revision: Union[str, None] = '1ca3924de304'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем таблицу users_new, если она существует
    op.execute("DROP TABLE IF EXISTS users_new")

    # Создаем новую таблицу с нужной структурой
    op.create_table(
        'users_new',
        sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_surname', sa.String(length=20), nullable=True),
        sa.Column('user_name', sa.String(length=20), nullable=True),
        sa.Column('phone', sa.String(length=12), nullable=True),
        sa.Column('email', sa.String(length=70), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.role_id'), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True, server_default=sa.func.now()),
        sa.Column('is_verified', sa.Boolean, nullable=True),
    )

    # Удаляем индекс, если он существует
    op.execute("DROP INDEX IF EXISTS ix_users_new_email")

    # Создаем индекс заново
    op.create_index('ix_users_new_email', 'users_new', ['email'], unique=True)

    # Копируем данные из старой таблицы
    op.execute("""
        INSERT INTO users_new (user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified)
        SELECT user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified FROM users
    """)

    # Удаляем старую таблицу
    op.drop_table('users')

    # Переименовываем новую таблицу в users
    op.rename_table('users_new', 'users')


def downgrade() -> None:
    op.create_table(
        'users_old',
        sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_surname', sa.String(length=20), nullable=True),
        sa.Column('user_name', sa.String(length=20), nullable=True),
        sa.Column('phone', sa.String(length=12), nullable=True),
        sa.Column('email', sa.String(length=70), unique=True, nullable=True, index=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.role_id'), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('is_verified', sa.Boolean, nullable=True),
    )

    op.execute("""
        INSERT INTO users_old (user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified)
        SELECT user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified FROM users
    """)

    op.drop_table('users')

    op.rename_table('users_old', 'users')

    op.create_index('ix_users_email', 'users', ['email'], unique=True)
