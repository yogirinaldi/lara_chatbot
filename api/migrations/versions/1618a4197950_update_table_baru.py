"""update table baru

Revision ID: 1618a4197950
Revises: 8a8c6f5392a9
Create Date: 2023-05-09 11:51:18.387777

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1618a4197950'
down_revision = '8a8c6f5392a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id_user', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nama', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('jk', sa.String(length=10), nullable=False),
    sa.Column('tanggal', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id_user')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=False)

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('nama',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.drop_index('ix_user_email')
        batch_op.create_index(batch_op.f('ix_admin_email'), ['email'], unique=False)

    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_data', sa.BigInteger(), autoincrement=True, nullable=False))
        batch_op.create_index(batch_op.f('ix_dataset_heading'), ['heading'], unique=False)
        batch_op.drop_column('id_dataset')

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_question', sa.BigInteger(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('id_user', sa.BigInteger(), nullable=True))
        batch_op.add_column(sa.Column('pertanyaan', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('jawaban', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('tanggal', sa.DateTime(), nullable=True))
        batch_op.drop_index('ix_question_ip_address')
        batch_op.create_foreign_key(None, 'user', ['id_user'], ['id_user'])
        batch_op.drop_column('id')
        batch_op.drop_column('ip_address')
        batch_op.drop_column('question')
        batch_op.drop_column('answer')
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('answer', mysql.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('question', mysql.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('ip_address', mysql.VARCHAR(length=15), nullable=False))
        batch_op.add_column(sa.Column('id', mysql.BIGINT(display_width=20), autoincrement=True, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_index('ix_question_ip_address', ['ip_address'], unique=False)
        batch_op.drop_column('tanggal')
        batch_op.drop_column('jawaban')
        batch_op.drop_column('pertanyaan')
        batch_op.drop_column('id_user')
        batch_op.drop_column('id_question')

    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_dataset', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False))
        batch_op.drop_index(batch_op.f('ix_dataset_heading'))
        batch_op.drop_column('id_data')

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_email'))
        batch_op.create_index('ix_user_email', ['email'], unique=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('nama',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
