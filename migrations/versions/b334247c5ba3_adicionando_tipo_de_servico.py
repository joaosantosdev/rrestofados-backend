"""adicionando tipo de servico

Revision ID: b334247c5ba3
Revises: 1c2876c32a15
Create Date: 2021-05-19 21:50:09.024813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b334247c5ba3'
down_revision = '1c2876c32a15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tipo_servico',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('servico', sa.Column('tipo_servico_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'servico', 'tipo_servico', ['tipo_servico_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'servico', type_='foreignkey')
    op.drop_column('servico', 'tipo_servico_id')
    op.drop_table('tipo_servico')
    # ### end Alembic commands ###