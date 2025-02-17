"""empty message

Revision ID: c52cd262ebd4
Revises: ae9464712a3c
Create Date: 2025-02-16 15:31:17.981486

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c52cd262ebd4'
down_revision = 'ae9464712a3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('h1_id', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.drop_column('h1_id')

    # ### end Alembic commands ###
