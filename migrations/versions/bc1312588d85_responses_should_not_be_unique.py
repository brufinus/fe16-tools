"""responses should not be unique

Revision ID: bc1312588d85
Revises: 1d81fbc3a976
Create Date: 2024-10-08 10:39:33.591576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc1312588d85'
down_revision = '1d81fbc3a976'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tea_final_topic', schema=None) as batch_op:
        batch_op.drop_index('ix_tea_final_topic_response')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tea_final_topic', schema=None) as batch_op:
        batch_op.create_index('ix_tea_final_topic_response', ['response'], unique=1)

    # ### end Alembic commands ###
