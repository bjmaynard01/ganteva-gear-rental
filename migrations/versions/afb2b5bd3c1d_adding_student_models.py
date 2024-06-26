"""adding student models

Revision ID: afb2b5bd3c1d
Revises: 4ecaee4d45b6
Create Date: 2024-04-11 11:59:06.033830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afb2b5bd3c1d'
down_revision = '4ecaee4d45b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.Date(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_student'))
    )
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_student_birthday'), ['birthday'], unique=False)
        batch_op.create_index(batch_op.f('ix_student_create_date'), ['create_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_student_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_student_last_name'), ['last_name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_student_last_name'))
        batch_op.drop_index(batch_op.f('ix_student_first_name'))
        batch_op.drop_index(batch_op.f('ix_student_create_date'))
        batch_op.drop_index(batch_op.f('ix_student_birthday'))

    op.drop_table('student')
    # ### end Alembic commands ###
