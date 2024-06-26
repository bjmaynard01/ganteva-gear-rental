"""renaming some fields

Revision ID: 31c984cb6418
Revises: ab37a46f99ac
Create Date: 2024-04-04 10:30:20.204457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31c984cb6418'
down_revision = 'ab37a46f99ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('end_date', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_end')
        batch_op.drop_column('date_start')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_start', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('date_end', sa.DATETIME(), nullable=True))
        batch_op.drop_column('end_date')
        batch_op.drop_column('start_date')

    # ### end Alembic commands ###
