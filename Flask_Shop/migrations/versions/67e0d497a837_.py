"""empty message

Revision ID: 67e0d497a837
Revises: 
Create Date: 2024-11-01 19:13:21.465625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67e0d497a837'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('pwd', sa.String(length=100), nullable=True),
    sa.Column('nick_name', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_users')
    # ### end Alembic commands ###