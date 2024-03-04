"""testing syntax changes

Revision ID: 36d3589416f0
Revises: 3ae5cf3fac65
Create Date: 2024-03-03 17:09:15.351386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36d3589416f0'
down_revision = '3ae5cf3fac65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gear_category', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.create_index(batch_op.f('ix_gear_category_name'), ['name'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('fname',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('lname',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('confirmed',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.drop_index('ix_user_username')
        batch_op.drop_index('ix_user_phone')
        batch_op.create_index(batch_op.f('ix_user_phone'), ['phone'], unique=False)
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(), nullable=False))
        batch_op.drop_index(batch_op.f('ix_user_phone'))
        batch_op.create_index('ix_user_phone', ['phone'], unique=1)
        batch_op.create_index('ix_user_username', ['username'], unique=1)
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.alter_column('confirmed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('lname',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('fname',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('gear_category', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_gear_category_name'))
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
