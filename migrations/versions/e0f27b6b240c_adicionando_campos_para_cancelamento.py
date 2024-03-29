"""adicionando campos para cancelamento

Revision ID: e0f27b6b240c
Revises: e0830729425c
Create Date: 2021-04-19 21:08:43.007324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0f27b6b240c'
down_revision = 'e0830729425c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('servico', sa.Column('cancelado', sa.Boolean(), nullable=True))
    op.add_column('servico', sa.Column('motivo', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('servico', 'motivo')
    op.drop_column('servico', 'cancelado')
    # ### end Alembic commands ###
