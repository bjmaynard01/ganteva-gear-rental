"""renaming category table and removing old syntax

Revision ID: cb5c54a78b01
Revises: ea274c14e766
Create Date: 2024-03-05 21:35:27.946920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb5c54a78b01'
down_revision = 'ea274c14e766'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gear_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('gear_categories', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_gear_categories_name'), ['name'], unique=False)

    with op.batch_alter_table('gear_category', schema=None) as batch_op:
        batch_op.drop_index('ix_gear_category_name')

    op.drop_table('gear_category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gear_category',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('gear_category', schema=None) as batch_op:
        batch_op.create_index('ix_gear_category_name', ['name'], unique=False)

    with op.batch_alter_table('gear_categories', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_gear_categories_name'))

    op.drop_table('gear_categories')
    # ### end Alembic commands ###