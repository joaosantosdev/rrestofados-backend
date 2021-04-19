"""criando servico

Revision ID: bd07d7a60407
Revises: 4f2278c02b63
Create Date: 2021-04-08 18:33:08.188305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd07d7a60407'
down_revision = '4f2278c02b63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('servico',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('descricao', sa.String(length=500), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('tecido_id', sa.BigInteger(), nullable=True),
    sa.Column('cor_id', sa.BigInteger(), nullable=True),
    sa.Column('data_entrega', sa.DateTime(), nullable=True),
    sa.Column('endereco_id', sa.BigInteger(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cor_id'], ['cor.id'], ),
    sa.ForeignKeyConstraint(['endereco_id'], ['endereco.id'], ),
    sa.ForeignKeyConstraint(['tecido_id'], ['tecido.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('servico')
    # ### end Alembic commands ###