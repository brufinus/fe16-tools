"""seed table

Revision ID: 2088e82667b0
Revises: 0086303a3c62
Create Date: 2024-10-10 01:01:16.153502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2088e82667b0'
down_revision = '0086303a3c62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('seed', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_seed_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seed', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_seed_name'))

    op.drop_table('seed')
    # ### end Alembic commands ###