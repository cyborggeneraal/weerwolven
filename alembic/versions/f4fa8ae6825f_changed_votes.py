"""changed votes

Revision ID: f4fa8ae6825f
Revises: a72dac824bc9
Create Date: 2023-04-25 19:37:31.672402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4fa8ae6825f'
down_revision = 'a72dac824bc9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('current_day', sa.Integer(), nullable=True))
    op.add_column('vote', sa.Column('vote_from', sa.String(), nullable=True))
    op.drop_column('vote', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vote', sa.Column('username', sa.VARCHAR(), nullable=True))
    op.drop_column('vote', 'vote_from')
    op.drop_column('game', 'current_day')
    # ### end Alembic commands ###