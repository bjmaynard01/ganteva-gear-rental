"""adding days of week and dates to classes

Revision ID: 9da70592cf83
Revises: 0b4b3668ed83
Create Date: 2024-04-04 08:44:55.510030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9da70592cf83'
down_revision = '0b4b3668ed83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_start', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date_end', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('monday', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('tuesday', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('wednesday', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('thursday', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('friday', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.drop_column('friday')
        batch_op.drop_column('thursday')
        batch_op.drop_column('wednesday')
        batch_op.drop_column('tuesday')
        batch_op.drop_column('monday')
        batch_op.drop_column('date_end')
        batch_op.drop_column('date_start')

    # ### end Alembic commands ###
