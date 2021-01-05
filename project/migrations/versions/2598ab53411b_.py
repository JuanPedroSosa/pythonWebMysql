"""empty message

Revision ID: 2598ab53411b
Revises: 
Create Date: 2020-04-22 16:36:41.031200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2598ab53411b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'updated_at')
    # ### end Alembic commands ###