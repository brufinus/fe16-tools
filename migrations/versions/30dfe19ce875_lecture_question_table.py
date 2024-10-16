"""lecture question table

Revision ID: 30dfe19ce875
Revises: 9493108fd8b7
Create Date: 2024-10-15 23:33:57.671045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30dfe19ce875'
down_revision = '9493108fd8b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lecture_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=256), nullable=False),
    sa.Column('answer', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('answer')
    )
    with op.batch_alter_table('lecture_question', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_lecture_question_question'), ['question'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lecture_question', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_lecture_question_question'))

    op.drop_table('lecture_question')
    # ### end Alembic commands ###
