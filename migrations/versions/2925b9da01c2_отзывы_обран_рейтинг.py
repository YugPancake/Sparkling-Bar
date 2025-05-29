"""отзывы, обран рейтинг

Revision ID: 2925b9da01c2
Revises: f11dd13f3314
Create Date: 2025-05-22 19:21:53.111411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
import datetime
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = '2925b9da01c2'
down_revision: Union[str, None] = 'f11dd13f3314'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Проверяем, существует ли таблица users_new
    if 'users_new' not in inspector.get_table_names():
        op.create_table(
            'users_new',
            sa.Column('user_id', sa.INTEGER(), primary_key=True, autoincrement=True),
            sa.Column('user_surname', sa.String(length=20), nullable=True),
            sa.Column('user_name', sa.String(length=20), nullable=True),
            sa.Column('phone', sa.String(length=12), nullable=True),
            sa.Column('email', sa.String(length=70), index=True, unique=True, nullable=True),
            sa.Column('password', sa.String(length=255), nullable=True),
            sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.role_id'), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.Column('is_verified', sa.Boolean(), default=False, nullable=False),
        )

        # Копируем данные из старой таблицы users в новую
        conn.execute(text("""
            INSERT INTO users_new (user_id, user_surname, user_name, phone, email, password, role_id, is_verified)
            SELECT user_id, user_surname, user_name, phone, email, password, role_id, is_verified FROM users
        """))

        # Удаляем старую таблицу users
        op.drop_table('users')

        # Переименовываем новую таблицу в users
        op.rename_table('users_new', 'users')
    else:
        print("Таблица users_new уже существует.")


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()

    # Создаем новую таблицу users с оригинальной структурой
    op.create_table(
        'users',
        sa.Column('user_id', sa.INTEGER(), primary_key=True, autoincrement=True),
        sa.Column('user_surname', sa.String(length=20), nullable=True),
        sa.Column('user_name', sa.String(length=20), nullable=True),
        sa.Column('phone', sa.String(length=12), nullable=True),
        sa.Column('email', sa.String(length=70), index=True, unique=True, nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.role_id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.now, nullable=False),
        sa.Column('is_verified', sa.Boolean(), default=False, nullable=False),
    )

    # Копируем данные из текущей таблицы users в новую
    conn.execute(text("""
        INSERT INTO users_new (user_id, user_surname, user_name, phone, email, password, role_id, is_verified)
        SELECT user_id, user_surname, user_name, phone, email, password, role_id, is_verified FROM users
    """))

    # Удаляем текущую таблицу users
    op.drop_table('users')

    # Переименовываем новую таблицу в users
    op.rename_table('users_new', 'users')
