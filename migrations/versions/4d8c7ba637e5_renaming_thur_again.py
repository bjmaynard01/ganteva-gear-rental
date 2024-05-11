"""renaming thur again

Revision ID: 4d8c7ba637e5
Revises: b4d7a571f003
Create Date: 2024-04-04 16:01:36.802462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d8c7ba637e5'
down_revision = 'b4d7a571f003'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thu', sa.Boolean(), nullable=False))
        batch_op.drop_column('thur')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thur', sa.BOOLEAN(), nullable=False))
        batch_op.drop_column('thu')

    # ### end Alembic commands ###
