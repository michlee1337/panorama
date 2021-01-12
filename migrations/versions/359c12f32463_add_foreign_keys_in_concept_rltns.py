"""add foreign keys in concept rltns

Revision ID: 359c12f32463
Revises: 3f3a0c542721
Create Date: 2021-01-08 16:18:09.677615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359c12f32463'
down_revision = '3f3a0c542721'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chunks', sa.Column('concept_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chunks', 'concepts', ['concept_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chunks', type_='foreignkey')
    op.drop_column('chunks', 'concept_id')
    # ### end Alembic commands ###
