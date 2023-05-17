"""empty message

Revision ID: 753199c30294
Revises: c2bb1d80e123
Create Date: 2023-05-15 11:06:48.490472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '753199c30294'
down_revision = 'c2bb1d80e123'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_admin', schema=None) as batch_op:
        batch_op.drop_column('admin')

    # ### end Alembic commands ###