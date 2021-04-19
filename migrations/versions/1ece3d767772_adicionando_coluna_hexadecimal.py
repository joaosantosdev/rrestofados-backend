"""Adicionando coluna hexadecimal 

Revision ID: 1ece3d767772
Revises: f2bed235d1b0
Create Date: 2021-02-08 19:25:53.384362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ece3d767772'
down_revision = 'f2bed235d1b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cor', sa.Column('hexadecimal', sa.String(length=15), nullable=True))
    op.alter_column('cor', 'descricao',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cor', 'descricao',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.drop_column('cor', 'hexadecimal')
    # ### end Alembic commands ###