"""rmv depth col from artifact

Revision ID: 8a7672413b17
Revises: 430d45c8d5a8
Create Date: 2021-01-11 17:06:30.065698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a7672413b17'
down_revision = '430d45c8d5a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artifacts', 'depth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artifacts', sa.Column('depth', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
