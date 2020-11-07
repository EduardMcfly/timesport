"""empty message

Revision ID: cf06267bd017
Revises: cb11801285ea
Create Date: 2020-11-01 17:00:53.410153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf06267bd017'
down_revision = 'cb11801285ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track_images',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('src', sa.String(length=90), nullable=True),
                    sa.Column('track_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['track_id'], ['tracks.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_images')
    # ### end Alembic commands ###