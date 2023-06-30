"""temp_user_organism_length_up

Revision ID: cd023436f99c
Revises: 6ec215fe023e
Create Date: 2023-06-30 14:30:02.641052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd023436f99c'
down_revision = '6ec215fe023e'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE utilisateurs.temp_users ALTER COLUMN organisme VARCHAR (250);")
    pass


def downgrade():
    pass
