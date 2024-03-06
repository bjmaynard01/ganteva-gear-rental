"""trying to move to mapped_columns

Revision ID: ea274c14e766
Revises: 36d3589416f0
Create Date: 2024-03-05 16:02:46.590923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea274c14e766'
down_revision = '36d3589416f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_classes_name'), ['name'], unique=False)

    with op.batch_alter_table('gear_category', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('fname',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('lname',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('confirmed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.drop_index('ix_user_phone')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('ix_user_phone', ['phone'], unique=False)
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.alter_column('confirmed',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('lname',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('fname',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('gear_category', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_classes_name'))

    op.drop_table('classes')
    # ### end Alembic commands ###