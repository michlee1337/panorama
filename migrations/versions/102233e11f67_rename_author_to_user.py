"""rename author to user

Revision ID: 102233e11f67
Revises: 8a7672413b17
Create Date: 2021-01-13 16:31:01.254850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '102233e11f67'
down_revision = '8a7672413b17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artifacts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('artifacts_author_id_fkey', 'artifacts', type_='foreignkey')
    op.create_foreign_key(None, 'artifacts', 'users', ['user_id'], ['id'])
    op.drop_column('artifacts', 'author_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artifacts', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'artifacts', type_='foreignkey')
    op.create_foreign_key('artifacts_author_id_fkey', 'artifacts', 'users', ['author_id'], ['id'])
    op.drop_column('artifacts', 'user_id')
    # ### end Alembic commands ###