"""1_0_17

Revision ID: 9cb3993e340e
Revises: d146dea51516
Create Date: 2024-03-28 14:36:35.588392

"""
import contextlib

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9cb3993e340e'
down_revision = 'd146dea51516'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with contextlib.suppress(Exception):
        with op.batch_alter_table("user") as batch_op:
            batch_op.add_column(sa.Column('is_otp', sa.BOOLEAN, server_default='0'))
            batch_op.add_column(sa.Column('otp_secret', sa.VARCHAR))
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
