"""Delete User back_popelates from invoice model

Revision ID: 8cf4706f3de7
Revises: f57664f2e6ac
Create Date: 2024-05-02 20:36:33.403199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cf4706f3de7'
down_revision: Union[str, None] = 'f57664f2e6ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###