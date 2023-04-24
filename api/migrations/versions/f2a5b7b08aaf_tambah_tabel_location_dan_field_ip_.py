"""tambah tabel location dan field ip_adrress di tabel question

Revision ID: f2a5b7b08aaf
Revises: d37f3da49e51
Create Date: 2023-04-24 09:19:38.686784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2a5b7b08aaf'
down_revision = 'd37f3da49e51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ip_address', sa.String(length=15), nullable=False))
        batch_op.create_index(batch_op.f('ix_question_ip_address'), ['ip_address'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_question_ip_address'))
        batch_op.drop_column('ip_address')

    # ### end Alembic commands ###
