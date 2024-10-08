"""tea final topic table

Revision ID: 1d81fbc3a976
Revises: adcbf687bd4f
Create Date: 2024-10-08 00:46:03.693191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d81fbc3a976'
down_revision = 'adcbf687bd4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tea_final_topic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=160), nullable=False),
    sa.Column('response', sa.String(length=64), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tea_final_topic', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tea_final_topic_comment'), ['comment'], unique=True)
        batch_op.create_index(batch_op.f('ix_tea_final_topic_response'), ['response'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tea_final_topic', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tea_final_topic_response'))
        batch_op.drop_index(batch_op.f('ix_tea_final_topic_comment'))

    op.drop_table('tea_final_topic')
    # ### end Alembic commands ###
