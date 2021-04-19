"""adicionando coluna cliente id 

Revision ID: e0830729425c
Revises: 7e35c25254d5
Create Date: 2021-04-15 20:29:34.006226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0830729425c'
down_revision = '7e35c25254d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('servico', sa.Column('cliente_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'servico', 'cliente', ['cliente_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'servico', type_='foreignkey')
    op.drop_column('servico', 'cliente_id')
    # ### end Alembic commands ###