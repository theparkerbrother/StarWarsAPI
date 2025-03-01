"""empty message

Revision ID: 8baebab59bb3
Revises: 295815cf2339
Create Date: 2025-03-01 17:06:50.936571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8baebab59bb3'
down_revision = '295815cf2339'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('home_planet_id', sa.Integer(), nullable=True))  # ✅ Allow NULL
        batch_op.create_foreign_key(None, 'planet', ['home_planet_id'], ['id'])


    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')  # Remove FK constraint first
        batch_op.drop_column('home_planet_id')  # Remove the column


    # ### end Alembic commands ###
