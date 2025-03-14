"""add ondelete actions to foreign keys

Revision ID: ddf85e430e4d
Revises: d55d1e1cc73f
Create Date: 2025-03-07 20:39:17.481041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddf85e430e4d'
down_revision: Union[str, None] = 'd55d1e1cc73f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('categories_user_id_fkey', 'categories', type_='foreignkey')
    op.create_foreign_key(None, 'categories', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'subscriptions', ['user_id'])
    op.drop_constraint('subscriptions_user_id_fkey', 'subscriptions', type_='foreignkey')
    op.create_foreign_key(None, 'subscriptions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('transactions_category_id_fkey', 'transactions', type_='foreignkey')
    op.drop_constraint('transactions_user_id_fkey', 'transactions', type_='foreignkey')
    op.create_foreign_key(None, 'transactions', 'categories', ['category_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'transactions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.create_foreign_key('transactions_user_id_fkey', 'transactions', 'users', ['user_id'], ['id'])
    op.create_foreign_key('transactions_category_id_fkey', 'transactions', 'categories', ['category_id'], ['id'])
    op.drop_constraint(None, 'subscriptions', type_='foreignkey')
    op.create_foreign_key('subscriptions_user_id_fkey', 'subscriptions', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'subscriptions', type_='unique')
    op.drop_constraint(None, 'categories', type_='foreignkey')
    op.create_foreign_key('categories_user_id_fkey', 'categories', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
