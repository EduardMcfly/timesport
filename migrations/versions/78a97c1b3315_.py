"""empty message

Revision ID: 78a97c1b3315
Revises: abafa1ed4a67
Create Date: 2020-10-20 21:25:44.036535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78a97c1b3315'
down_revision = 'abafa1ed4a67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    # ### end Alembic commands ###
