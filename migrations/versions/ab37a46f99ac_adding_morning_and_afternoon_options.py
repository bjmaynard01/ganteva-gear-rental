"""adding morning and afternoon options

Revision ID: ab37a46f99ac
Revises: 9da70592cf83
Create Date: 2024-04-04 08:59:10.024025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab37a46f99ac'
down_revision = '9da70592cf83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('morning', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('afternoon', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.drop_column('afternoon')
        batch_op.drop_column('morning')

    # ### end Alembic commands ###