"""как сойти с этой планеты

Revision ID: 1ca3924de304
Revises: 2925b9da01c2
Create Date: 2025-05-29 19:32:16.987171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ca3924de304'
down_revision: Union[str, None] = '2925b9da01c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Удаляем таблицу users_new, если она существует
    op.drop_table('users_new', if_exists=True)  # if_exists=True не поддерживается в SQLite, просто удалите эту строку

    # Создаем новую таблицу users_new с нужными параметрами
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
        sa.Column('is_verified', sa.Boolean(), nullable=True),  # Изменяем на nullable=True
    )

    # Копируем данные из старой таблицы users в новую
    op.execute("""
        INSERT INTO users_new (user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified)
        SELECT user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified FROM users
    """)

    # Удаляем старую таблицу users
    op.drop_table('users')

    # Переименовываем новую таблицу в users
    op.rename_table('users_new', 'users')

def downgrade() -> None:
    """Downgrade schema."""
    # Создаем новую таблицу users_new с предыдущей структурой
    op.create_table(
        'users_new',
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('user_surname', sa.VARCHAR(length=20), nullable=True),
        sa.Column('user_name', sa.VARCHAR(length=20), nullable=True),
        sa.Column('phone', sa.VARCHAR(length=12), nullable=True),
        sa.Column('email', sa.VARCHAR(length=70), nullable=True),
        sa.Column('password', sa.VARCHAR(length=255), nullable=True),
        sa.Column('role_id', sa.INTEGER(), nullable=True),
        sa.Column('created_at', sa.DATETIME(), nullable=False),
        sa.Column('is_verified', sa.BOOLEAN(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.role_id']),
        sa.PrimaryKeyConstraint('user_id')
    )

    # Копируем данные обратно из таблицы users в users_new
    op.execute("""
        INSERT INTO users_new (user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified)
        SELECT user_id, user_surname, user_name, phone, email, password, role_id, created_at, is_verified FROM users
    """)

    # Удаляем новую таблицу users
    op.drop_table('users')

    # Переименовываем users_new обратно в users
    op.rename_table('users_new', 'users')

    # Восстанавливаем индекс
    op.create_index('ix_users_new_email', 'users', ['email'], unique=True)
