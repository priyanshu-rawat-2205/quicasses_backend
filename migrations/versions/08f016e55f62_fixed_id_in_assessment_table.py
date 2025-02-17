"""fixed ID in assessment table

Revision ID: 08f016e55f62
Revises: c52cd262ebd4
Create Date: 2025-02-17 10:35:18.993496

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '08f016e55f62'
down_revision = 'c52cd262ebd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.drop_column('h1_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('h1_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###
