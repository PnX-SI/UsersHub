"""UsersHub samples data

Revision ID: f63a8f44c969
Revises: 
Create Date: 2021-09-06 18:17:06.392398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f63a8f44c969'
down_revision = None
branch_labels = ('usershub-samples',)
depends_on = (
    '9445a69f2bed',  # usershub
    '72f227e37bdf',  # utilisateurs schema samples data
)


def upgrade():
    op.execute("""
    INSERT INTO utilisateurs.cor_role_app_profil (id_role, id_application, id_profil) VALUES
    (
        (SELECT id_role FROM utilisateurs.t_roles WHERE nom_role = 'Grp_admin'),
        (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'UH'),
        (SELECT id_profil FROM utilisateurs.t_profils WHERE code_profil = '6')
    )
    """)


def downgrade():
    op.execute("""
    DELETE FROM utilisateurs.cor_role_app_profil cor
    USING
        utilisateurs.t_roles r,
        utilisateurs.t_applications a,
        utilisateurs.t_profils p
    WHERE
            cor.id_role = r.id_role
        AND cor.id_application = a.id_application
        AND cor.id_profil = p.id_profil
        AND r.nom_role = 'Grp_admin'
        AND a.code_application = 'UH'
        AND p.code_profil = '6'
    """)
