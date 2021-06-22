"""criando tabela fluxo de caixa

Revision ID: c23bdda83919
Revises: 3f907ab649a1
Create Date: 2021-05-20 17:59:19.926494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c23bdda83919'
down_revision = '3f907ab649a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fluxo_caixa',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('descricao', sa.String(length=200), nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fluxo_caixa')
    # ### end Alembic commands ###