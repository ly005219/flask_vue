"""Increase pwd field length

Revision ID: 10e509518865
Revises: 67e0d497a837
Create Date: 2024-11-02 21:41:08.297056

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '10e509518865'
down_revision = '67e0d497a837'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_users', schema=None) as batch_op:
        batch_op.alter_column('pwd',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=800),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_users', schema=None) as batch_op:
        batch_op.alter_column('pwd',
               existing_type=sa.String(length=800),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###
