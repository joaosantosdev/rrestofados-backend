"""empty message

Revision ID: c2984dc6474e
Revises: 1f24e842142c
Create Date: 2021-03-07 16:38:29.709712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2984dc6474e'
down_revision = '1f24e842142c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cliente',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('cpf', sa.String(length=15), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('endereco_id', sa.BigInteger(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['endereco_id'], ['endereco.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('telefone',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('numero', sa.String(length=20), nullable=False),
    sa.Column('descricao', sa.String(length=100), nullable=False),
    sa.Column('whatsapp', sa.Boolean(), nullable=False),
    sa.Column('cliente_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('endereco', sa.Column('estado_id', sa.BigInteger(), nullable=True))
    op.drop_constraint('endereco_estadoId_fkey', 'endereco', type_='foreignkey')
    op.create_foreign_key(None, 'endereco', 'estado', ['estado_id'], ['id'])
    op.drop_column('endereco', 'estadoId')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('endereco', sa.Column('estadoId', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'endereco', type_='foreignkey')
    op.create_foreign_key('endereco_estadoId_fkey', 'endereco', 'estado', ['estadoId'], ['id'])
    op.drop_column('endereco', 'estado_id')
    op.drop_table('telefone')
    op.drop_table('cliente')
    # ### end Alembic commands ###