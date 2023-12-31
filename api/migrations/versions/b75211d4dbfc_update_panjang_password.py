"""update panjang password

Revision ID: b75211d4dbfc
Revises: e2826ae766d2
Create Date: 2023-06-01 18:09:36.520024

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b75211d4dbfc'
down_revision = 'e2826ae766d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=102),
               existing_nullable=False)

    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.drop_index('ix_dataset_heading')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.create_index('ix_dataset_heading', ['heading'], unique=False)

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=102),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
