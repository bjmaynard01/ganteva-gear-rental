"""adding student class relationships

Revision ID: 0eca3a624a29
Revises: afb2b5bd3c1d
Create Date: 2024-04-14 14:30:30.331283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0eca3a624a29'
down_revision = 'afb2b5bd3c1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes_students_ref',
    sa.Column('classes_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['classes_id'], ['student.id'], name=op.f('fk_classes_students_ref_classes_id_student')),
    sa.ForeignKeyConstraint(['student_id'], ['classes.id'], name=op.f('fk_classes_students_ref_student_id_classes'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('classes_students_ref')
    # ### end Alembic commands ###
