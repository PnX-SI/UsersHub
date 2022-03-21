"""upgrade utilisateurs schema

Revision ID: 6ec215fe023e
Revises: 9445a69f2bed
Create Date: 2021-09-30 16:29:25.531376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ec215fe023e'
down_revision = '9445a69f2bed'
branch_labels = None
depends_on = (
    '951b8270a1cf',  # utilisateurs
)


def upgrade():
    pass


def downgrade():
    pass
